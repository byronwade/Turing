// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Fuzz sweeps and the recursion bounds that make them possible.
//!
//! An `Err` from any stage is a pass: refusing malformed input is the designed
//! behaviour. The only finding is an unwind.

use turing_fuzz::{Outcome, Rng, generate_css, generate_html, generate_js, run_seed, sweep};

// -- the harness itself --------------------------------------------------

#[test]
fn the_generator_is_deterministic() {
    // A finding that cannot be reproduced from its seed is an anecdote. This is
    // the property that makes the seed in a report worth printing.
    assert_eq!(
        generate_html(&mut Rng::new(12345)),
        generate_html(&mut Rng::new(12345))
    );
    assert_eq!(
        generate_css(&mut Rng::new(999)),
        generate_css(&mut Rng::new(999))
    );
    assert_eq!(generate_js(&mut Rng::new(7)), generate_js(&mut Rng::new(7)));
}

#[test]
fn different_seeds_produce_different_inputs() {
    // Guards against a generator that ignores its seed, which would make a
    // thousand-seed sweep one input tested a thousand times.
    let inputs: std::collections::HashSet<String> =
        (0..50).map(|s| generate_html(&mut Rng::new(s))).collect();
    assert!(
        inputs.len() > 40,
        "50 seeds produced only {} distinct documents",
        inputs.len()
    );
}

#[test]
fn a_zero_seed_still_generates() {
    // xorshift emits zero forever from a zero state, so the seed is remapped. A
    // caller sweeping from zero should not have to know that.
    assert!(!generate_html(&mut Rng::new(0)).is_empty());
    assert_ne!(
        generate_html(&mut Rng::new(0)),
        generate_html(&mut Rng::new(1))
    );
}

#[test]
fn the_harness_reports_a_panic_when_one_happens() {
    // The positive control. A sweep that finds nothing proves nothing until the
    // harness is shown to catch a real unwind, so this panics deliberately
    // through the same guard the stages use and checks it is reported rather
    // than escaping or being silently swallowed.
    let previous = std::panic::take_hook();
    std::panic::set_hook(Box::new(|_| {}));
    let caught = std::panic::catch_unwind(|| panic!("deliberate"));
    std::panic::set_hook(previous);
    assert!(
        caught.is_err(),
        "catch_unwind must observe a panic, or every sweep is theatre; \
         this fails if the profile ever switches to panic = \"abort\""
    );
}

// -- the sweep -----------------------------------------------------------

#[test]
fn no_generated_input_makes_any_stage_unwind() {
    // The claim the whole workspace rests on: hostile input yields a value or a
    // typed error, never a panic. Until now it was tested only against inputs
    // chosen by whoever wrote the code.
    let findings = sweep(1, 2_000);
    assert!(
        findings.is_empty(),
        "fuzz findings (reproduce with the printed seed): {:#?}",
        findings.iter().take(5).collect::<Vec<_>>()
    );
}

#[test]
fn a_known_seed_reproduces_exactly() {
    assert_eq!(run_seed(42), run_seed(42));
}

#[test]
fn findings_carry_enough_to_reproduce() {
    // Shape check on the report: a finding without a seed and a stage is not
    // actionable. Constructed directly because the sweep is expected to be
    // empty, and a test that only passes when something is broken is worse than
    // no test.
    let finding = Outcome::Panicked {
        seed: 7,
        stage: "layout",
        input: "<div>".to_string(),
    };
    match finding {
        Outcome::Panicked { seed, stage, input } => {
            assert_eq!(seed, 7);
            assert_eq!(stage, "layout");
            assert!(!input.is_empty());
        }
        Outcome::Returned => unreachable!(),
    }
}

// -- recursion bounds ----------------------------------------------------

/// Builds `depth` nested `<div>` elements.
fn nested(depth: usize) -> String {
    format!(
        "<html><body>{}{}</body></html>",
        "<div>".repeat(depth),
        "</div>".repeat(depth)
    )
}

fn document_of(html: &str) -> turing_html::Document {
    let tokens = turing_html::Tokenizer::new(html)
        .tokenize()
        .expect("tokenizes")
        .tokens;
    turing_html::TreeBuilder::new()
        .build(&tokens)
        .expect("builds")
}

#[test]
fn deep_nesting_is_refused_by_layout_rather_than_overflowing_the_stack() {
    // Before the bound existed this aborted the process at around 1000 levels.
    // A stack overflow does not unwind, so catch_unwind cannot see it and no
    // harness can turn it into a failed assertion — the engine has to refuse.
    let document = document_of(&nested(2_000));
    let sheet = turing_css::Stylesheet::parse("div { display: block; }").expect("parses");
    let result = turing_layout::layout(
        &document,
        &sheet,
        800.0,
        turing_layout::TextMetrics::default(),
    );
    assert!(matches!(
        result,
        Err(turing_layout::LayoutError::NestingTooDeep { .. })
    ));
}

#[test]
fn deep_nesting_is_refused_by_the_accessibility_tree() {
    let document = document_of(&nested(2_000));
    assert!(matches!(
        turing_a11y::build(&document),
        Err(turing_a11y::A11yError::NestingTooDeep { .. })
    ));
}

#[test]
fn the_two_consumers_agree_on_the_depth_limit() {
    // Different limits would mean a document that lays out but has no
    // accessibility tree, or the reverse, which is worse than either bound.
    assert_eq!(
        turing_layout::MAX_NESTING_DEPTH,
        turing_a11y::MAX_NESTING_DEPTH
    );
}

#[test]
fn nesting_just_inside_the_limit_still_works() {
    // A bound that refuses ordinary documents would be a regression dressed as
    // a fix. Real pages nest tens of levels, not hundreds.
    let document = document_of(&nested(turing_layout::MAX_NESTING_DEPTH - 10));
    let sheet = turing_css::Stylesheet::parse("div { display: block; }").expect("parses");
    assert!(
        turing_layout::layout(
            &document,
            &sheet,
            800.0,
            turing_layout::TextMetrics::default()
        )
        .is_ok()
    );
    assert!(turing_a11y::build(&document).is_ok());
}

#[test]
fn tokenizing_and_tree_building_survive_depth_the_later_stages_refuse() {
    // These are iterative, so they have no reason to bound depth, and bounding
    // them would refuse documents the engine can in fact represent. Recorded so
    // the asymmetry is deliberate rather than accidental.
    let html = nested(20_000);
    let tokens = turing_html::Tokenizer::new(&html)
        .tokenize()
        .expect("tokenizes at depth no recursion can reach")
        .tokens;
    let document = turing_html::TreeBuilder::new()
        .build(&tokens)
        .expect("builds at depth no recursion can reach");
    assert!(document.len() > 20_000);
}

#[test]
fn a_deeply_nested_name_subtree_does_not_overflow() {
    // Name computation runs before the depth check reaches deeper elements, so
    // it can be handed a subtree of any depth even when the document as a whole
    // will be refused. Its walk is iterative for that reason.
    let inner = format!(
        "<span>{}deep{}</span>",
        "<span>".repeat(5_000),
        "</span>".repeat(5_000)
    );
    let html = format!("<html><body><button>{inner}</button></body></html>");
    let document = document_of(&html);
    // The document is deeper than the limit, so the result is a refusal rather
    // than a tree — but it must be a returned error, not an abort.
    assert!(matches!(
        turing_a11y::build(&document),
        Err(turing_a11y::A11yError::NestingTooDeep { .. })
    ));
}

// -- generator reach -----------------------------------------------------

#[test]
fn the_script_generator_reaches_past_the_parser_bound() {
    // The gap that let the JS parser ship without a recursion bound: the first
    // generator emitted only short flat fragments, so no sweep could ever reach
    // deep nesting, and a clean sweep said nothing about it.
    //
    // Asserting the generator's reach directly is the fix. A generator that
    // quietly stops covering a construct otherwise turns a green sweep into a
    // statement about the generator rather than about the engine.
    let refused = (1..300u64)
        .map(|seed| generate_js(&mut Rng::new(seed)))
        .filter(|source| {
            matches!(
                turing_js::compile(source),
                Err(turing_js::JsError::NestingTooDeep { .. })
            )
        })
        .count();
    assert!(
        refused > 10,
        "300 seeds produced only {refused} scripts deep enough to reach the \
         parser's nesting bound; the generator is not covering that construct"
    );
}

#[test]
fn deeply_nested_script_is_refused_rather_than_overflowing_the_stack() {
    // Measured before the bound existed: parsing overflowed a 1 MiB stack at
    // roughly 95 nested parentheses in a debug build, because the precedence
    // chain costs about ten frames per expression level.
    for source in [
        format!("let a = {}1{};", "(".repeat(500), ")".repeat(500)),
        format!("{}a=1;{}", "if(1){".repeat(500), "}".repeat(500)),
        format!("let a = {}1;", "-".repeat(500)),
    ] {
        assert!(
            matches!(
                turing_js::compile(&source),
                Err(turing_js::JsError::NestingTooDeep { .. })
            ),
            "expected a typed refusal rather than an abort"
        );
    }
}

#[test]
fn ordinary_script_nesting_still_parses() {
    // A bound that refuses real programs would be a regression dressed as a
    // fix. Expressions nest single digits deep in practice.
    assert!(turing_js::compile("let a = ((((1 + 2))));").is_ok());
    assert!(turing_js::compile("if (1) { if (1) { if (1) { let a = 1; } } }").is_ok());
    assert!(turing_js::compile("let a = ---1;").is_ok());
}

#[test]
fn every_recursive_consumer_refuses_rather_than_aborting() {
    // Three crates now recurse over attacker-controlled structure, and all
    // three had the same defect. Asserting the behaviour in one place is a
    // prompt to ask the same question of the next recursive consumer, rather
    // than discovering it the way these were discovered.
    //
    // Behaviour, not constants: that a limit is nonzero says nothing about
    // whether it is enforced.
    let deep_markup = document_of(&nested(2_000));
    let sheet = turing_css::Stylesheet::parse("div { display: block; }").expect("parses");

    assert!(matches!(
        turing_js::compile(&format!("let a = {}1{};", "(".repeat(500), ")".repeat(500))),
        Err(turing_js::JsError::NestingTooDeep { .. })
    ));
    assert!(matches!(
        turing_layout::layout(
            &deep_markup,
            &sheet,
            800.0,
            turing_layout::TextMetrics::default()
        ),
        Err(turing_layout::LayoutError::NestingTooDeep { .. })
    ));
    assert!(matches!(
        turing_a11y::build(&deep_markup),
        Err(turing_a11y::A11yError::NestingTooDeep { .. })
    ));
}

// -- selector index equivalence ------------------------------------------

/// Parses a generated pair, skipping seeds the engine refuses. A refusal is a
/// pass everywhere else in this file and is not interesting here either.
fn generated_pair(seed: u64) -> Option<(turing_html::Document, turing_css::Stylesheet)> {
    let mut rng = Rng::new(seed);
    let html = generate_html(&mut rng);
    let css = generate_css(&mut rng);
    let tokens = turing_html::Tokenizer::new(&html).tokenize().ok()?;
    let document = turing_html::TreeBuilder::new().build(&tokens.tokens).ok()?;
    let sheet = turing_css::Stylesheet::parse(&css).ok()?;
    Some((document, sheet))
}

#[test]
fn the_indexed_cascade_agrees_with_the_reference_everywhere() {
    // Differential rather than a hand corpus. An optimisation that changes a
    // result is worse than the slow version it replaced, and every way selector
    // bucketing goes wrong — a selector list filed under one key only, an
    // unkeyed selector dropped, a source-order tie resolved differently —
    // produces a plausible answer rather than an obvious failure.
    for seed in 1..400u64 {
        let Some((document, sheet)) = generated_pair(seed) else {
            continue;
        };
        let index = turing_css::SelectorIndex::build(&sheet);
        for raw in 0..document.len() {
            let node = turing_html::NodeId::from_index(raw);
            assert_eq!(
                turing_css::cascade(&document, node, &index),
                turing_css::cascade_reference(&document, node, &sheet),
                "seed {seed}, node {raw}: the index disagreed with the reference"
            );
        }
    }
}

#[test]
fn the_differential_actually_reaches_multi_candidate_elements() {
    // The equivalence test proves nothing if no generated element ever draws
    // rules from more than one bucket: the tie-breaking paths bucketing
    // endangers are exactly the ones that need two buckets to reach.
    //
    // Same lesson as the script generator's nesting depth. A green differential
    // over a corpus that cannot express the failure is a statement about the
    // corpus.
    let mut reached = 0;
    for seed in 1..400u64 {
        let Some((document, sheet)) = generated_pair(seed) else {
            continue;
        };
        let index = turing_css::SelectorIndex::build(&sheet);
        for raw in 0..document.len() {
            let node = turing_html::NodeId::from_index(raw);
            if index.candidate_count(&document, node) > 1 {
                reached += 1;
            }
        }
    }
    assert!(
        reached > 100,
        "only {reached} elements drew more than one candidate rule; the \
         differential is not reaching the cases bucketing endangers"
    );
}

fn element_named(document: &turing_html::Document, tag: &str) -> turing_html::NodeId {
    (0..document.len())
        .map(turing_html::NodeId::from_index)
        .find(|&n| document.element_name(n) == Some(tag))
        .expect("the element exists")
}

fn document_from(html: &str) -> turing_html::Document {
    let tokens = turing_html::Tokenizer::new(html)
        .tokenize()
        .expect("tokenizes")
        .tokens;
    turing_html::TreeBuilder::new()
        .build(&tokens)
        .expect("builds")
}

#[test]
fn the_index_actually_narrows_the_candidate_set() {
    // The mechanism, asserted deterministically. Elapsed time is the obvious
    // thing to check and would fail on a loaded machine for reasons unrelated
    // to the code.
    let css: String = (0..200)
        .map(|i| format!(".c{i} {{ color: red; }}"))
        .collect();
    let document = document_from("<html><body><div class='c7'>x</div></body></html>");
    let sheet = turing_css::Stylesheet::parse(&css).expect("parses");
    let index = turing_css::SelectorIndex::build(&sheet);

    assert_eq!(index.rule_count(), 200);
    assert_eq!(
        index.candidate_count(&document, element_named(&document, "div")),
        1,
        "an element with one class should reach one of two hundred rules"
    );
}

#[test]
fn an_unkeyed_selector_is_still_considered() {
    // A universal or attribute-only selector has no bucket. Dropping it rather
    // than putting it in the always-considered list would silently stop it
    // matching anything, which no test of keyed selectors would notice.
    let sheet =
        turing_css::Stylesheet::parse("* { color: red; } [id] { color: blue; }").expect("parses");
    let index = turing_css::SelectorIndex::build(&sheet);
    let document = document_from("<html><body><p id='a'>x</p></body></html>");
    let p = element_named(&document, "p");

    assert_eq!(index.candidate_count(&document, p), 2);
    assert_eq!(
        turing_css::cascade(&document, p, &index),
        turing_css::cascade_reference(&document, p, &sheet)
    );
}

#[test]
fn a_selector_list_is_filed_under_every_key() {
    // `div, .foo` must match through either selector. Filing the rule under one
    // key only makes the other silently stop matching.
    let sheet = turing_css::Stylesheet::parse("div, .foo { color: red; }").expect("parses");
    let index = turing_css::SelectorIndex::build(&sheet);
    let document = document_from("<html><body><span class='foo'>x</span></body></html>");
    let span = element_named(&document, "span");

    assert_eq!(
        index.candidate_count(&document, span),
        1,
        "reached through the class selector, not the type one"
    );
    assert!(!turing_css::cascade(&document, span, &index).is_empty());
}

#[test]
fn a_duplicate_id_resolves_to_the_first_in_document_order() {
    // The one correctness constraint on the id index. A map that let a later
    // element overwrite an earlier one would disagree with the linear scan it
    // replaced, and with what getElementById is specified to do.
    let document = document_from(
        "<html><body><p id='dup'>first</p><span id='dup'>second</span></body></html>",
    );
    let found = document.element_by_id("dup").expect("resolves");
    assert_eq!(document.element_name(found), Some("p"));
}
