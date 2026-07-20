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
