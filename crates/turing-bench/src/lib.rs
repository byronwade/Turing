// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Per-stage timing harness for the rendering pipeline.
//!
//! # Why this exists
//!
//! `PB-013` forbids any performance claim that is not backed by measurement.
//! This crate is the measurement. It does not compare against another engine —
//! there is no comparison data, and producing a number next to a competitor's
//! name without a controlled methodology would be the exact overclaiming the
//! blueprint prohibits. Every figure here is a raw baseline, useful only for
//! tracking this engine against its own past.
//!
//! # Why not a benchmarking crate
//!
//! The workspace takes no external dependencies. `criterion` and its peers are
//! out for that reason alone, so what is borrowed is the methodology rather
//! than the code: discard warm-up iterations, run a fixed sample count, and
//! report order statistics rather than a mean.
//!
//! # What is measured
//!
//! Each pipeline stage separately — tokenize, tree-build, parse CSS, cascade,
//! layout — rather than one end-to-end number. "Where does the time go" is the
//! question that makes a baseline actionable; a single total hides a stage
//! regressing while another improves.
//!
//! # What these numbers are not
//!
//! Wall-clock timings on a developer machine. They vary with CPU scaling, other
//! load, and allocator state. They are deliberately not wired into any
//! validator: a noisy measurement used as a gate produces flaky failures and
//! trains people to ignore it. Treat a change of a few percent as noise.

#![forbid(unsafe_code)]

use std::time::{Duration, Instant};

use turing_css::{Color, SelectorIndex, Stylesheet, cascade};
use turing_html::{Document, Tokenizer, TreeBuilder};
use turing_layout::{TextMetrics, build_display_list, layout};
use turing_paint::{PaintList, paint};
use turing_raster::rasterize;

/// How many iterations to run before recording, letting caches and the
/// allocator reach steady state.
pub const WARMUP: usize = 20;

/// How many recorded iterations each measurement takes.
pub const SAMPLES: usize = 100;

/// The timing distribution for one stage, with the statistical treatment
/// `PB-013` and the benchmark book's statistics chapter require before a
/// number may be read as evidence rather than an anecdote.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Measurement {
    /// Fastest observed iteration. The least contaminated by unrelated load,
    /// and so the most stable figure to compare across runs.
    pub min: Duration,
    /// Median iteration.
    pub median: Duration,
    /// Slowest observed iteration. Worth watching: a max far above the median
    /// usually means an allocation or growth step, not measurement noise.
    pub max: Duration,
    /// The 25th and 75th percentiles. The interquartile range between them is
    /// the spread of the middle half, unmoved by the tail a single scheduling
    /// hiccup drags out.
    pub p25: Duration,
    pub p75: Duration,
    /// A distribution-free 95% confidence interval for the median, from the
    /// order statistics — no assumption that the timings are normal, which
    /// they are not (they are right-skewed by scheduling). If two runs'
    /// intervals do not overlap, their medians differ for a reason beyond
    /// this run's noise.
    pub median_ci_low: Duration,
    pub median_ci_high: Duration,
    /// Coefficient of variation in parts per thousand: the standard deviation
    /// as a fraction of the mean. The single-number noise indicator — a stage
    /// with a high CoV is measuring the machine as much as the code, and its
    /// comparisons deserve less weight.
    pub cov_permille: u32,
}

impl Measurement {
    /// Times `operation` over [`WARMUP`] discarded then [`SAMPLES`] recorded
    /// iterations.
    ///
    /// The closure returns a value which is handed to [`consume`] so the
    /// optimiser cannot delete the work as unused.
    pub fn of<T, F: FnMut() -> T>(mut operation: F) -> Self {
        for _ in 0..WARMUP {
            consume(operation());
        }

        let mut samples = Vec::with_capacity(SAMPLES);
        for _ in 0..SAMPLES {
            let start = Instant::now();
            let produced = operation();
            samples.push(start.elapsed());
            consume(produced);
        }

        samples.sort_unstable();
        Self::from_sorted(&samples)
    }

    /// Computes the distribution from an already-sorted sample slice.
    ///
    /// Separated from timing so the statistics are testable against known
    /// inputs without running a clock.
    #[must_use]
    fn from_sorted(samples: &[Duration]) -> Self {
        assert!(
            !samples.is_empty(),
            "a measurement needs at least one sample"
        );
        let n = samples.len();
        let percentile = |fraction: f64| {
            // Nearest-rank: the smallest sample at or above the fraction.
            let rank = (fraction * n as f64).ceil() as usize;
            samples[rank.saturating_sub(1).min(n - 1)]
        };

        // Distribution-free 95% CI for the median via the normal approximation
        // to the binomial ranks: the median sits between the order statistics
        // at n/2 +/- 1.96*sqrt(n)/2. Clamped so a small sample still yields a
        // valid (if wide) interval.
        let half = n as f64 / 2.0;
        let spread = 1.96 * (n as f64).sqrt() / 2.0;
        let low_rank = (half - spread).floor().max(0.0) as usize;
        let high_rank = ((half + spread).ceil() as usize).min(n - 1);

        // Coefficient of variation from the mean and population standard
        // deviation, in nanoseconds.
        let nanos: Vec<f64> = samples.iter().map(|d| d.as_nanos() as f64).collect();
        let mean = nanos.iter().sum::<f64>() / n as f64;
        let variance = nanos.iter().map(|v| (v - mean).powi(2)).sum::<f64>() / n as f64;
        let cov_permille = if mean > 0.0 {
            (variance.sqrt() / mean * 1000.0).round() as u32
        } else {
            0
        };

        Self {
            min: samples[0],
            median: samples[n / 2],
            max: samples[n - 1],
            p25: percentile(0.25),
            p75: percentile(0.75),
            median_ci_low: samples[low_rank],
            median_ci_high: samples[high_rank],
            cov_permille,
        }
    }

    /// Whether `self` is a regression against `baseline`.
    ///
    /// A practical threshold, not a bare comparison: a run is a regression
    /// only when its median exceeds the baseline's by more than
    /// `min_effect_permille` (a deliberate effect size, screening out changes
    /// too small to matter) **and** the two medians' confidence intervals do
    /// not overlap (screening out changes that are only this run's noise).
    /// Both gates must pass, which is what keeps a control chart from crying
    /// wolf on a quiet machine's jitter.
    #[must_use]
    pub fn is_regression(&self, baseline: &Self, min_effect_permille: u32) -> bool {
        let effect_gate = {
            let base = baseline.median.as_nanos();
            let threshold = base + base * u128::from(min_effect_permille) / 1000;
            self.median.as_nanos() > threshold
        };
        // Intervals are disjoint when this run's low bound is above the
        // baseline's high bound.
        let separated = self.median_ci_low > baseline.median_ci_high;
        effect_gate && separated
    }
}

/// Prevents the optimiser from removing work whose result is unused.
///
/// `std::hint::black_box` is the supported way to express this; without it a
/// stage whose output is dropped can legally be compiled away, and the harness
/// would report a suspiciously fast time for work that never happened.
fn consume<T>(value: T) {
    std::hint::black_box(&value);
}

/// One stage's name and timing.
#[derive(Clone, Debug)]
pub struct StageResult {
    pub stage: &'static str,
    pub measurement: Measurement,
}

/// The document every stage is measured against.
///
/// Deliberately small and hand-written rather than a captured real page. A real
/// page would exercise constructs this engine refuses by design, so the run
/// would measure error paths. This is representative of what the engine
/// currently implements, and it should grow as the engine does — at which point
/// the baselines reset and old numbers stop being comparable, which is worth
/// noting in the log when it happens.
pub const DOCUMENT: &str = r"<!DOCTYPE html>
<html>
  <body>
    <div class='page'>
      <h1>Turing</h1>
      <p class='lead'>A browser engine written from the specifications.</p>
      <p>Block and inline formatting, margin collapse, and greedy line breaking
         are implemented. Constructs that would change where content lands are
         refused rather than approximated.</p>
      <div class='row'><span>one</span><span>two</span><span>three</span></div>
      <p>Trailing paragraph so the block stacking path has more than one
         sibling to walk.</p>
    </div>
  </body>
</html>";

/// The stylesheet every stage is measured against.
pub const STYLESHEET: &str = r"
body { display: block; margin: 8px; }
div { display: block; }
h1 { display: block; margin: 16px; }
p { display: block; margin: 12px; color: #222222; }
p.lead { color: #000000; }
span { display: inline; }
.page { background: #ffffff; width: 800px; }
.row { display: block; background: #eeeeee; }
";

/// Runs every stage and returns their timings in pipeline order.
///
/// # Panics
///
/// Panics if the fixture document or stylesheet fails to parse. That is a
/// defect in this crate rather than a runtime condition: the fixtures are
/// constants chosen to stay inside what the engine implements.
#[must_use]
pub fn run() -> Vec<StageResult> {
    let tokens = Tokenizer::new(DOCUMENT)
        .tokenize()
        .expect("fixture document tokenizes")
        .tokens;
    let document = TreeBuilder::new()
        .build(&tokens)
        .expect("fixture document builds");
    let stylesheet = Stylesheet::parse(STYLESHEET).expect("fixture stylesheet parses");
    let elements = element_nodes(&document);

    vec![
        StageResult {
            stage: "tokenize",
            measurement: Measurement::of(|| {
                Tokenizer::new(DOCUMENT).tokenize().expect("tokenizes")
            }),
        },
        StageResult {
            stage: "tree-build",
            measurement: Measurement::of(|| TreeBuilder::new().build(&tokens).expect("builds")),
        },
        StageResult {
            stage: "parse-css",
            measurement: Measurement::of(|| Stylesheet::parse(STYLESHEET).expect("parses")),
        },
        StageResult {
            stage: "cascade",
            measurement: Measurement::of(|| {
                // The index is built inside the measurement because that is
                // what a real style pass does: once per stylesheet, not once
                // per element. Excluding it would report a cost nobody pays.
                let index = SelectorIndex::build(&stylesheet);
                // Every element, so the figure scales with the document rather
                // than reflecting whichever single node was picked.
                let mut matched = 0;
                for &element in &elements {
                    matched += cascade(&document, element, &index, None).len();
                }
                matched
            }),
        },
        StageResult {
            stage: "layout",
            measurement: Measurement::of(|| {
                layout(&document, &stylesheet, 1280.0, TextMetrics::default(), None)
                    .expect("lays out")
            }),
        },
        StageResult {
            stage: "display-list",
            measurement: Measurement::of(|| {
                let root = layout(&document, &stylesheet, 1280.0, TextMetrics::default(), None)
                    .expect("lays out");
                build_display_list(&root)
            }),
        },
        StageResult {
            stage: "paint",
            measurement: Measurement::of(|| {
                let root = layout(&document, &stylesheet, 1280.0, TextMetrics::default(), None)
                    .expect("lays out");
                let list = PaintList::from_display_list(&build_display_list(&root));
                paint(
                    &list,
                    1280,
                    720,
                    Color {
                        red: 255,
                        green: 255,
                        blue: 255,
                    },
                )
                .expect("paints")
            }),
        },
        StageResult {
            stage: "raster",
            measurement: Measurement::of(|| {
                let root = layout(&document, &stylesheet, 1280.0, TextMetrics::default(), None)
                    .expect("lays out");
                let list = build_display_list(&root);
                rasterize(
                    &list,
                    1280,
                    720,
                    Color {
                        red: 255,
                        green: 255,
                        blue: 255,
                    },
                )
                .expect("rasterizes")
            }),
        },
    ]
}

/// Collects every element node in the document, in document order.
fn element_nodes(document: &Document) -> Vec<turing_html::NodeId> {
    let mut found = Vec::new();
    let mut stack = vec![document.root()];
    while let Some(node) = stack.pop() {
        if document.element_name(node).is_some() {
            found.push(node);
        }
        stack.extend(document.node(node).children.iter().rev().copied());
    }
    found
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_pipeline_stage_is_measured() {
        // Guards against a stage being dropped from the harness while the
        // reported baselines still look complete.
        let stages: Vec<_> = run().iter().map(|r| r.stage).collect();
        assert_eq!(
            stages,
            vec![
                "tokenize",
                "tree-build",
                "parse-css",
                "cascade",
                "layout",
                "display-list",
                "paint",
                "raster"
            ]
        );
    }

    #[test]
    fn measurements_are_ordered() {
        let measurement = Measurement::of(|| Stylesheet::parse(STYLESHEET).expect("parses"));
        assert!(measurement.min <= measurement.p25);
        assert!(measurement.p25 <= measurement.median);
        assert!(measurement.median <= measurement.p75);
        assert!(measurement.p75 <= measurement.max);
        assert!(measurement.median_ci_low <= measurement.median);
        assert!(measurement.median <= measurement.median_ci_high);
    }

    /// A known sample set makes the statistics checkable without a clock.
    fn from_micros(values: &[u64]) -> Measurement {
        let mut samples: Vec<Duration> = values.iter().map(|&v| Duration::from_micros(v)).collect();
        samples.sort_unstable();
        Measurement::from_sorted(&samples)
    }

    #[test]
    fn the_statistics_match_a_known_sample_set() {
        // 0..=100 microseconds: median 50, quartiles at 25 and 75, and a
        // tight-enough distribution that its CoV is a stable known figure.
        let values: Vec<u64> = (0..=100).collect();
        let m = from_micros(&values);
        assert_eq!(m.median, Duration::from_micros(50));
        assert_eq!(m.p25, Duration::from_micros(25));
        assert_eq!(m.p75, Duration::from_micros(75));
        // A uniform 0..=100 distribution has CoV ~ 0.577/... near 58%.
        assert!(
            (550..=600).contains(&m.cov_permille),
            "uniform CoV near 58%: {}",
            m.cov_permille
        );
        // The median CI brackets the median and is narrower than the full
        // range.
        assert!(m.median_ci_low < m.median && m.median < m.median_ci_high);
        assert!(m.median_ci_high - m.median_ci_low < m.max - m.min);
    }

    #[test]
    fn regression_needs_both_a_real_effect_and_separated_intervals() {
        // Baseline and a run 20% slower with no overlap: a regression.
        let baseline = from_micros(&(90..=110).collect::<Vec<_>>());
        let slower = from_micros(&(190..=210).collect::<Vec<_>>());
        assert!(
            slower.is_regression(&baseline, 50),
            "clear slowdown flagged"
        );

        // A run only marginally slower, intervals overlapping: not a
        // regression, because it is within this run's noise.
        let jitter = from_micros(&(92..=112).collect::<Vec<_>>());
        assert!(
            !jitter.is_regression(&baseline, 50),
            "overlapping intervals are noise, not regression"
        );

        // A real, separated slowdown that is nonetheless below the effect
        // threshold is screened out: statistically clear, practically trivial.
        let tiny = from_micros(&(111..=131).collect::<Vec<_>>());
        assert!(
            !tiny.is_regression(&baseline, 500),
            "a sub-threshold effect is not a regression even when separated"
        );
    }

    #[test]
    fn the_fixtures_stay_inside_what_the_engine_implements() {
        // If a future change makes the engine refuse a construct in the
        // fixture, the harness would silently start timing an error path.
        let tokens = Tokenizer::new(DOCUMENT)
            .tokenize()
            .expect("tokenizes")
            .tokens;
        let document = TreeBuilder::new().build(&tokens).expect("builds");
        let stylesheet = Stylesheet::parse(STYLESHEET).expect("parses");
        assert!(layout(&document, &stylesheet, 1280.0, TextMetrics::default(), None).is_ok());
    }
}
