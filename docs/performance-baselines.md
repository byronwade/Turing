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

**These rows are not disjoint and must not be summed.** `layout` calls
`resolve_style`, which calls `cascade`, once per element — so the cascade work
measured on its own row is also running inside the layout row. Box generation
and block layout proper account for roughly the difference, about 3 µs, not the
full 6.4 µs. Adding the five figures together double-counts the cascade and
produces a "pipeline total" that does not correspond to any real run.

They are measured separately anyway, because a stage that only ever appears
inside another cannot be attributed when it regresses. Read the table as five
independent measurements, not a breakdown of one.

Environment: Windows 11, `x86_64-pc-windows-msvc`, release profile. Absolute
figures are not portable across machines; the shape of the distribution and the
relative cost of the stages are the parts worth reading.

Two observations, recorded without acting on them yet:

- Tokenizing is the most expensive stage, and by a wider margin than the table
  first suggests: once the cascade is subtracted from layout, tokenizing costs
  more than twice layout proper. It is the stage that touches every input byte,
  so this is expected rather than anomalous, but it is where optimisation effort
  would pay first.
- Layout's maximum sits well above its median while every other stage is tight.
  That asymmetry is consistent with allocation during box-tree construction. It
  is a hypothesis, not a finding — confirming it needs allocation profiling that
  does not exist yet.

## Scaling

Baselines above measure one small document. They say nothing about how cost
grows, and growth is where an engine becomes unusable while every test still
passes.

Two paths were quadratic in document size. Measured 2026-07-20, release build,
before and after indexing:

| Case | n | Before | After |
| --- | --- | --- | --- |
| Style + layout, n rules over n elements | 200 | 1.4 ms | 0.7 ms |
| | 400 | 8.3 ms | 1.3 ms |
| | 800 | 27.7 ms | 2.8 ms |
| | 1600 | 95.5 ms | 4.9 ms |
| Accessibility tree, n `aria-labelledby` refs over n ids | 200 | 0.3 ms | 0.2 ms |
| | 400 | 0.9 ms | 0.4 ms |
| | 800 | 3.2 ms | 1.0 ms |
| | 1600 | 18.9 ms | 2.7 ms |

Read the growth, not the absolute figures. Before, eight times the input cost
roughly sixty-seven times the work in both cases — the signature of an O(n²)
path. After, cost per element is roughly flat across the range.

Causes and fixes: the cascade evaluated every rule against every element, now
narrowed by `turing_css::SelectorIndex`; and `aria-labelledby` resolved each
IDREF with a linear document scan, now a map owned by the document.

A third was found later, in tokenizing. Dropping a duplicate attribute was a
scan of the attributes collected so far, so an element's attribute count was
quadratic:

| Attributes on one element | Before | After |
| --- | --- | --- |
| 2,000 | 3.3 ms | 1.3 ms |
| 8,000 | 80.3 ms | 4.0 ms |
| 16,000 | — | 9.7 ms |
| 32,000 | — | 18.5 ms |

Four times the input cost twenty-four times the work, from markup a page emits
in one line. A set of seen names replaces the scan; the attribute vector still
owns source order and first-occurrence-wins.

Five other pathological shapes were measured at the same time and are all
linear: one enormous text node, many sibling elements, many unmatched close
tags, a long unterminated comment, and many declarations in one block.

**The index only removes work that could not have matched.** A stylesheet of
`div` rules against a document of `div` elements is still quadratic, because
every pair genuinely matches and no index can help. The improvement above is on
selective selectors, which is what real stylesheets contain.

The regression guard for this is a deterministic count of candidate rules, not
a timing assertion. Wall-clock in a test suite fails on a loaded machine for
reasons unrelated to the code.

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
