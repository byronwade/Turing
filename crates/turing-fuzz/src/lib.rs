// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Deterministic fuzz harness for the engine's hostile-input surfaces.
//!
//! # What this is evidence for
//!
//! `IF-003`, the static engine semantic contract, lists four evidence items:
//! `WP-006` through `WP-009`, WPT and reduced tests, fuzzing, and full-versus-
//! incremental equivalence. This crate is the third. It does **not** complete
//! the freeze — WPT is an external corpus import and there is no incremental
//! path to compare against yet — and so it does not unblock `WP-015`.
//!
//! # The claim under test
//!
//! Every parser in this workspace claims that hostile input produces either a
//! result or a typed error, never a panic and never a hang. Until now that
//! claim was tested only against hand-written cases, which is to say against
//! inputs chosen by the same person who wrote the code.
//!
//! An `Err` is a **pass** here, not a failure. Refusing malformed input is the
//! designed behaviour. The only findings are an unwind and a hang.
//!
//! # Determinism
//!
//! No system randomness and no wall-clock. Every input derives from a `u64`
//! seed through the PRNG below, so a failure reproduces exactly from the seed
//! printed alongside it. A fuzz finding that cannot be reproduced is an anecdote.
//!
//! # What this harness cannot catch
//!
//! A stack overflow aborts the process; it does not unwind, so
//! [`std::panic::catch_unwind`] never sees it. That is not a gap to work around
//! but a reason the engine must bound its own recursion — which is why
//! `turing_layout::MAX_NESTING_DEPTH` exists. Generated nesting here stays
//! within a bound for that reason, and the deep-nesting case is tested
//! separately with the depth limit as its expected answer.
//!
//! This harness also runs only under an unwinding panic strategy. The release
//! profile sets `panic = "abort"`, so it is a test-profile tool by construction.

#![forbid(unsafe_code)]

use std::panic::{AssertUnwindSafe, catch_unwind};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::mpsc;
use std::time::Duration;

/// A small deterministic pseudo-random generator.
///
/// xorshift64*, chosen because it is a dozen lines that can be read and
/// verified rather than trusted. Statistical quality beyond "spreads bits
/// around" is irrelevant here: the generator picks between grammar branches,
/// it does not need to survive a randomness test suite.
#[derive(Clone, Debug)]
pub struct Rng {
    state: u64,
}

impl Rng {
    /// Creates a generator from `seed`.
    ///
    /// A zero seed would make xorshift emit zero forever, so it is remapped
    /// rather than rejected — a caller sweeping a seed range should not have to
    /// know to skip one.
    #[must_use]
    pub fn new(seed: u64) -> Self {
        Self {
            state: if seed == 0 {
                0x9E37_79B9_7F4A_7C15
            } else {
                seed
            },
        }
    }

    /// Returns the next value.
    pub fn next_u64(&mut self) -> u64 {
        let mut x = self.state;
        x ^= x >> 12;
        x ^= x << 25;
        x ^= x >> 27;
        self.state = x;
        x.wrapping_mul(0x2545_F491_4F6C_DD1D)
    }

    /// Returns a value below `bound`, or zero when `bound` is zero.
    pub fn below(&mut self, bound: usize) -> usize {
        if bound == 0 {
            return 0;
        }
        (self.next_u64() % bound as u64) as usize
    }

    /// Picks an element of `options`.
    ///
    /// # Panics
    ///
    /// Panics when `options` is empty, which is a defect in a generator rather
    /// than something an input can cause.
    pub fn pick<'a, T>(&mut self, options: &'a [T]) -> &'a T {
        assert!(!options.is_empty(), "cannot pick from an empty slice");
        let index = self.below(options.len());
        &options[index]
    }

    /// Returns true with probability `1 / n`.
    pub fn one_in(&mut self, n: usize) -> bool {
        self.below(n.max(1)) == 0
    }
}

/// Tag names, class names, and ids shared by the markup and stylesheet
/// generators.
///
/// Deliberately tiny. The first version of these generators drew selectors and
/// attributes from unrelated pools, so a generated element almost never matched
/// more than one generated rule — 400 seeds produced 14 elements with more than
/// one candidate rule, which made the cascade differential very nearly vacuous.
///
/// A small shared vocabulary makes collisions the common case instead of the
/// rare one, which is what puts elements in several selector buckets at once
/// and exercises specificity and source-order tie-breaking.
pub mod vocabulary {
    /// Element names both generators use.
    pub const TAGS: &[&str] = &["div", "p", "span", "a"];
    /// Class names both generators use.
    pub const CLASSES: &[&str] = &["one", "two", "three"];
    /// Id values both generators use.
    pub const IDS: &[&str] = &["x", "y"];
}

/// The deepest nesting a generator will emit.
///
/// Below `turing_layout::MAX_NESTING_DEPTH` so the general sweep exercises the
/// normal path rather than repeatedly hitting the depth refusal. Deep nesting is
/// a separate, deliberate case.
pub const GENERATED_DEPTH_LIMIT: usize = 12;

/// The deepest expression and statement nesting the script generator emits.
///
/// Unlike the markup limit, this deliberately exceeds the engine's own bound
/// (`turing_js::MAX_NESTING_DEPTH`), so sweeps cover both sides of it. Nesting
/// past the bound must produce a typed refusal, and that is only tested if the
/// generator can reach it.
pub const GENERATED_JS_DEPTH_LIMIT: usize = 200;

/// Generates a document that is plausible HTML but not necessarily valid.
///
/// Structure-aware rather than uniformly random bytes: random bytes almost
/// always fail in the first few tokenizer states and never reach tree
/// construction, so they test one shallow layer thoroughly and everything else
/// not at all. This emits real tags, real attributes, and then corrupts them.
#[must_use]
pub fn generate_html(rng: &mut Rng) -> String {
    // The shared vocabulary first, so those tags dominate, then the wider set
    // so structural and refusal paths are still reached.
    const TAGS: &[&str] = &[
        "div", "p", "span", "a", "div", "p", "span", "a", "h1", "ul", "li", "nav", "header",
        "footer", "img", "input", "button", "script", "style", "table", "template",
    ];
    const ATTRS: &[&str] = &[
        "id",
        "class",
        "href",
        "aria-label",
        "aria-labelledby",
        "aria-hidden",
        "role",
        "alt",
        "type",
        "title",
        "style",
    ];
    // Values chosen to reach refusal paths as well as success paths.
    const VALUES: &[&str] = &[
        "a",
        "one two",
        "true",
        "false",
        "presentation",
        "",
        "tablist",
        "\"",
        "'",
        "<",
        "&amp;",
        "\u{0}",
        "text",
        "button",
    ];

    let mut out = String::from("<html><body>");
    let mut open: Vec<&str> = Vec::new();

    for _ in 0..rng.below(40) + 1 {
        match rng.below(10) {
            0..=4 if open.len() < GENERATED_DEPTH_LIMIT => {
                let tag = *rng.pick(TAGS);
                out.push('<');
                out.push_str(tag);
                for _ in 0..rng.below(3) {
                    out.push(' ');
                    // Class and id are drawn from the shared vocabulary most of
                    // the time, so generated elements collide with generated
                    // selectors. Without this the cascade differential almost
                    // never sees an element in more than one selector bucket.
                    let (attribute, value) = if rng.one_in(3) {
                        ("class", *rng.pick(vocabulary::CLASSES))
                    } else if rng.one_in(4) {
                        ("id", *rng.pick(vocabulary::IDS))
                    } else {
                        (*rng.pick(ATTRS), *rng.pick(VALUES))
                    };
                    out.push_str(attribute);
                    out.push_str("='");
                    out.push_str(value);
                    // Sometimes leave the quote unterminated.
                    if !rng.one_in(8) {
                        out.push('\'');
                    }
                }
                // Sometimes leave the tag unterminated.
                if rng.one_in(10) {
                    out.push('<');
                } else {
                    out.push('>');
                    open.push(tag);
                }
            }
            5..=6 => {
                if let Some(tag) = open.pop() {
                    out.push_str("</");
                    out.push_str(tag);
                    out.push('>');
                }
            }
            // A close tag that does not match anything open.
            7 => {
                out.push_str("</");
                out.push_str(rng.pick(TAGS));
                out.push('>');
            }
            8 => out.push_str(rng.pick(VALUES)),
            _ => {
                out.push_str("<!--");
                out.push_str(rng.pick(VALUES));
                if !rng.one_in(6) {
                    out.push_str("-->");
                }
            }
        }
    }

    // Deliberately do not close what remains open: unclosed elements at end of
    // input are one of the cases a tree builder most easily gets wrong.
    out.push_str("</body></html>");
    out
}

/// Generates a stylesheet that is plausible CSS but not necessarily valid.
#[must_use]
pub fn generate_css(rng: &mut Rng) -> String {
    const PROPERTIES: &[&str] = &[
        "display",
        "width",
        "height",
        "margin",
        "padding",
        "border-width",
        "color",
        "background",
        "float",
        "position",
        "writing-mode",
        "unknown-property",
    ];
    const VALUES: &[&str] = &[
        "block",
        "inline",
        "none",
        "flex",
        "grid",
        "10px",
        "-5px",
        "0",
        "auto",
        "50%",
        "#fff",
        "#abcdef",
        "red",
        "rebeccapurple",
        "rgb(1,2,3)",
        "left",
        "absolute",
        "vertical-rl",
        "",
    ];

    let mut out = String::new();
    for _ in 0..rng.below(12) + 1 {
        out.push_str(&selector(rng));
        out.push_str(" {");
        for _ in 0..rng.below(4) {
            out.push_str(rng.pick(PROPERTIES));
            out.push(':');
            out.push_str(rng.pick(VALUES));
            if !rng.one_in(8) {
                out.push(';');
            }
        }
        // Sometimes leave the block unterminated.
        if !rng.one_in(10) {
            out.push('}');
        }
    }
    out
}

/// Builds one selector, mostly from the shared vocabulary.
///
/// Selector lists and compound selectors are generated rather than drawn from a
/// fixed table, because both are where the selector index can go wrong: a list
/// must be filed under every one of its keys, and a compound must be filed
/// under the most specific one.
fn selector(rng: &mut Rng) -> String {
    // Malformed and unsupported selectors, kept so refusal paths stay covered.
    // Ordinary selectors are built from the shared vocabulary instead, by
    // `selector` below.
    const ODD_SELECTORS: &[&str] = &[
        "a[href]",
        "*",
        "li:first-child",
        "::before",
        "@media screen",
        "div,",
        "",
    ];
    if rng.one_in(6) {
        return (*rng.pick(ODD_SELECTORS)).to_string();
    }

    let mut parts = Vec::new();
    for _ in 0..rng.below(2) + 1 {
        let mut one = String::new();
        // A descendant or child combinator, sometimes, so ancestor matching is
        // exercised alongside subject matching.
        if rng.one_in(4) {
            one.push_str(rng.pick(vocabulary::TAGS));
            one.push_str(if rng.one_in(2) { " > " } else { " " });
        }
        match rng.below(4) {
            0 => one.push_str(rng.pick(vocabulary::TAGS)),
            1 => {
                one.push('.');
                one.push_str(rng.pick(vocabulary::CLASSES));
            }
            2 => {
                one.push('#');
                one.push_str(rng.pick(vocabulary::IDS));
            }
            _ => {
                // A compound: tag and class together, which must be filed under
                // the class rather than the tag.
                one.push_str(rng.pick(vocabulary::TAGS));
                one.push('.');
                one.push_str(rng.pick(vocabulary::CLASSES));
            }
        }
        parts.push(one);
    }
    parts.join(", ")
}

/// Generates a script that is plausible JavaScript but not necessarily valid.
#[must_use]
pub fn generate_js(rng: &mut Rng) -> String {
    const FRAGMENTS: &[&str] = &[
        "let a = 1;",
        "var b = a + 2;",
        "if (a) { a = 2; } else { a = 3; }",
        "while (a) { a = a - 1; }",
        "a = (1 + 2) * 3;",
        "function f() { return 1; }",
        "a = f(",
        "a = {};",
        "a = [1, 2];",
        "class C {}",
        "try { a } catch (e) {}",
        "a = 'unterminated",
        "a = 0x;",
        "a === b;",
        "return;",
        "}",
        "((((",
    ];
    let mut out = String::new();
    for _ in 0..rng.below(10) + 1 {
        out.push_str(rng.pick(FRAGMENTS));
        out.push('\n');
    }

    // Nesting, generated explicitly rather than left to emerge from short
    // fragments. The first version of this generator emitted only flat
    // statements, and the JS parser's missing recursion bound was found by hand
    // afterwards rather than by a sweep: a generator that cannot express a
    // construct cannot find a defect in it.
    //
    // The depth range straddles `turing_js::MAX_NESTING_DEPTH` so sweeps cover
    // both the accepted and the refused side of the bound.
    let depth = rng.below(GENERATED_JS_DEPTH_LIMIT);
    match rng.below(3) {
        0 => {
            out.push_str("let deep = ");
            out.push_str(&"(".repeat(depth));
            out.push('1');
            out.push_str(&")".repeat(depth));
            out.push_str(";\n");
        }
        1 => {
            out.push_str(&"if (1) {".repeat(depth));
            out.push_str("let d = 1;");
            out.push_str(&"}".repeat(depth));
            out.push('\n');
        }
        _ => {
            out.push_str("let deep = ");
            out.push_str(&"-".repeat(depth));
            out.push_str("1;\n");
        }
    }
    out
}

/// What a fuzz iteration produced.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum Outcome {
    /// The stage returned, with either a value or a typed error. Both pass.
    Returned,
    /// The stage unwound.
    Panicked {
        seed: u64,
        stage: &'static str,
        input: String,
    },
    /// The sweep stopped making progress.
    ///
    /// Reported separately from a panic because the cause is different in kind:
    /// an unwind is a defect the code noticed, a hang is one it did not. The
    /// seed is whichever was in flight when the deadline passed, which is where
    /// to start looking rather than a proven culprit — the seed before it may
    /// have been the slow one.
    HungAt { seed: u64 },
}

/// Runs `body`, returning its value or the finding if it unwound.
///
/// Returns the value rather than just a verdict so a stage runs **once**. An
/// earlier version guarded a stage and then re-ran it unguarded to obtain its
/// output for the next stage; a panic in the second call escaped the harness
/// entirely and surfaced as a raw backtrace with no seed. The positive control
/// caught that, which is what a positive control is for.
///
/// `AssertUnwindSafe` is needed because the closures borrow local state. It
/// asserts a property of this harness, not of the code under test: nothing here
/// observes partially-mutated state after a panic, because the next iteration
/// regenerates its input from a seed.
fn guard<T, F: FnOnce() -> T>(
    seed: u64,
    stage: &'static str,
    input: &str,
    body: F,
) -> Result<T, Outcome> {
    // Panic output would otherwise bury the seed in noise. The previous hook is
    // restored so a genuine failure elsewhere still reports normally.
    let previous = std::panic::take_hook();
    std::panic::set_hook(Box::new(|_| {}));
    let result = catch_unwind(AssertUnwindSafe(body));
    std::panic::set_hook(previous);

    result.map_err(|_| Outcome::Panicked {
        seed,
        stage,
        input: input.to_string(),
    })
}

/// Records a finding and yields `None`, so the pipeline stops descending
/// without losing it.
///
/// A free function rather than a closure because each stage returns a different
/// type, and a closure would be monomorphised to whichever one it saw first.
fn collect<T>(result: Result<T, Outcome>, findings: &mut Vec<Outcome>) -> Option<T> {
    match result {
        Ok(value) => Some(value),
        Err(finding) => {
            findings.push(finding);
            None
        }
    }
}

/// Runs every input surface for one seed and returns any findings.
///
/// Each stage is guarded separately so a finding names the stage that produced
/// it rather than "somewhere in the pipeline". A stage that returns `Err` is a
/// pass — refusing malformed input is the designed behaviour — and simply
/// leaves nothing to feed the stages below it.
#[must_use]
pub fn run_seed(seed: u64) -> Vec<Outcome> {
    let mut findings = Vec::new();
    let mut rng = Rng::new(seed);

    let html = generate_html(&mut rng);
    let css = generate_css(&mut rng);
    let js = generate_js(&mut rng);

    let tokenized = collect(
        guard(seed, "tokenize", &html, || {
            turing_html::Tokenizer::new(&html).tokenize()
        }),
        &mut findings,
    );
    let parsed_css = collect(
        guard(seed, "parse-css", &css, || {
            turing_css::Stylesheet::parse(&css)
        }),
        &mut findings,
    );
    collect(
        guard(seed, "parse-js", &js, || turing_js::compile(&js)),
        &mut findings,
    );

    let Some(Ok(tokenized)) = tokenized else {
        return findings;
    };
    let tokens = tokenized.tokens;

    let built = collect(
        guard(seed, "tree-build", &html, || {
            turing_html::TreeBuilder::new().build(&tokens)
        }),
        &mut findings,
    );
    let Some(Ok(document)) = built else {
        return findings;
    };

    collect(
        guard(seed, "accessibility", &html, || {
            turing_a11y::build(&document)
        }),
        &mut findings,
    );

    if let Some(Ok(stylesheet)) = parsed_css {
        collect(
            guard(seed, "layout", &html, || {
                turing_layout::layout(
                    &document,
                    &stylesheet,
                    800.0,
                    turing_layout::TextMetrics::default(),
                )
            }),
            &mut findings,
        );
    }

    findings
}

/// Runs seeds `first..first + count` and returns every finding.
#[must_use]
pub fn sweep(first: u64, count: u64) -> Vec<Outcome> {
    (first..first + count).flat_map(run_seed).collect()
}

/// Runs a sweep under a deadline, reporting a hang if it stops progressing.
///
/// # Why this exists
///
/// [`catch_unwind`] observes a panic. It cannot observe a loop that never
/// finishes, and an input that makes a parser spin is as effective a denial of
/// service as one that makes it crash — more so, because it consumes the
/// processor while doing it. Sweeping without this checks half the claim the
/// engine makes about hostile input.
///
/// # Why a watchdog rather than a proof
///
/// Termination is not decidable in general and these parsers are not written in
/// a form that makes it checkable, so the honest instrument is an observation:
/// work that normally finishes in milliseconds has not finished in `budget`.
///
/// The budget should be enormous relative to the work, so it fires on a genuine
/// hang rather than on a loaded machine. A tight deadline here would be a flaky
/// test, which is worse than no test because it teaches people to rerun rather
/// than look.
///
/// # Reporting
///
/// The in-flight seed is per-call rather than a global. A process-wide counter
/// was the obvious shape and is wrong: test harnesses run tests in parallel, so
/// two sweeps would overwrite each other's progress and each would report a
/// seed from the other. It starts at `first`, so a deadline that passes before
/// any work completes still names a seed from this sweep instead of zero.
///
/// A hang leaves the worker thread running, since a stuck thread cannot be
/// killed safely. The process is expected to be a test binary about to fail.
#[must_use]
pub fn sweep_under_deadline(first: u64, count: u64, budget: Duration) -> Vec<Outcome> {
    let in_flight = std::sync::Arc::new(AtomicU64::new(first));
    let worker_progress = std::sync::Arc::clone(&in_flight);
    let (sender, receiver) = mpsc::channel();

    std::thread::spawn(move || {
        let mut findings = Vec::new();
        for seed in first..first + count {
            worker_progress.store(seed, Ordering::Relaxed);
            findings.extend(run_seed(seed));
        }
        // A closed channel means the watchdog already gave up; nothing to do.
        let _ = sender.send(findings);
    });

    match receiver.recv_timeout(budget) {
        Ok(findings) => findings,
        Err(_) => vec![Outcome::HungAt {
            seed: in_flight.load(Ordering::Relaxed),
        }],
    }
}
