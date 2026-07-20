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

use turing_css::{SelectorIndex, Stylesheet, cascade};
use turing_html::{Document, Tokenizer, TreeBuilder};
use turing_layout::{TextMetrics, layout};

/// How many iterations to run before recording, letting caches and the
/// allocator reach steady state.
pub const WARMUP: usize = 20;

/// How many recorded iterations each measurement takes.
pub const SAMPLES: usize = 100;

/// The timing distribution for one stage.
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
        Self {
            min: samples[0],
            median: samples[SAMPLES / 2],
            max: samples[SAMPLES - 1],
        }
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
                    matched += cascade(&document, element, &index).len();
                }
                matched
            }),
        },
        StageResult {
            stage: "layout",
            measurement: Measurement::of(|| {
                layout(&document, &stylesheet, 1280.0, TextMetrics::default()).expect("lays out")
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
            vec!["tokenize", "tree-build", "parse-css", "cascade", "layout"]
        );
    }

    #[test]
    fn measurements_are_ordered() {
        let measurement = Measurement::of(|| Stylesheet::parse(STYLESHEET).expect("parses"));
        assert!(measurement.min <= measurement.median);
        assert!(measurement.median <= measurement.max);
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
        assert!(layout(&document, &stylesheet, 1280.0, TextMetrics::default()).is_ok());
    }
}
