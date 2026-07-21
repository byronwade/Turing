// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Fuzz sweeps and the recursion bounds that make them possible.
//!
//! An `Err` from any stage is a pass: refusing malformed input is the designed
//! behaviour. The only finding is an unwind.

use std::time::Duration;
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
        Outcome::Returned | Outcome::HungAt { .. } => unreachable!(),
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
        None,
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
            turing_layout::TextMetrics::default(),
            None
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
    // Spaced triple negation parses as three nested unary minuses.
    assert!(turing_js::compile("let a = - - -1;").is_ok());
    // Unspaced `---1` is not the same program: the lexer takes `--` by
    // maximal munch (the same rule real JS tokenizers use, and the one that
    // makes `--`/`++` lex at all), leaving `- 1` as the operand of a prefix
    // decrement — which is not an assignable target, so this is refused
    // rather than silently reinterpreted as triple negation. Real JS engines
    // reject `---1` the same way (SyntaxError), so this refusal is the
    // spec-correct reading, not a regression.
    assert!(turing_js::compile("let a = ---1;").is_err());
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
            turing_layout::TextMetrics::default(),
            None
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
                turing_css::cascade(&document, node, &index, None),
                turing_css::cascade_reference(&document, node, &sheet, None),
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
        turing_css::cascade(&document, p, &index, None),
        turing_css::cascade_reference(&document, p, &sheet, None)
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
    assert!(!turing_css::cascade(&document, span, &index, None).is_empty());
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

// -- termination ---------------------------------------------------------

#[test]
fn no_generated_input_makes_a_sweep_stop_progressing() {
    // catch_unwind observes a panic; it cannot observe a loop that never ends.
    // An input that makes a parser spin is as effective a denial of service as
    // one that makes it crash, and sweeping without a deadline checks half the
    // claim the engine makes about hostile input.
    //
    // The budget is enormous relative to the work — this sweep finishes in a
    // few seconds — so it fires on a genuine hang rather than on a loaded
    // machine. A tight deadline would be a flaky test, which is worse than no
    // test because it teaches people to rerun rather than look.
    let findings = turing_fuzz::sweep_under_deadline(1, 1_000, Duration::from_secs(120));
    assert!(
        findings.is_empty(),
        "sweep findings: {:#?}",
        findings.iter().take(5).collect::<Vec<_>>()
    );
}

#[test]
fn the_watchdog_reports_a_hang_when_one_happens() {
    // Positive control for the deadline, matching the one for the panic guard.
    // A deadline that never fires is indistinguishable from one that cannot,
    // and the previous three times a check went unverified here it turned out
    // to be measuring nothing.
    //
    // A zero budget makes the deadline pass before any real work completes,
    // which exercises the timeout path itself rather than a real hang.
    let findings = turing_fuzz::sweep_under_deadline(1, 1_000_000, Duration::from_millis(0));
    assert!(
        matches!(findings.as_slice(), [Outcome::HungAt { .. }]),
        "expected a hang report, got {findings:#?}"
    );
}

#[test]
fn a_hang_report_names_the_seed_in_flight() {
    let findings = turing_fuzz::sweep_under_deadline(7, 1_000_000, Duration::from_millis(0));
    match findings.as_slice() {
        [Outcome::HungAt { seed }] => assert!(*seed >= 7, "seed {seed} is from this sweep"),
        other => panic!("expected a hang report, got {other:#?}"),
    }
}

// -- attribute handling --------------------------------------------------

#[test]
fn many_attributes_stay_linear_and_specified() {
    // Duplicate-attribute dropping reads as "check the ones collected so far"
    // and was implemented as a scan per attribute, which is quadratic in
    // attribute count: 3.3 ms for two thousand attributes on one element, 80 ms
    // for eight thousand, from markup a page emits in a line.
    //
    // Asserted as behaviour rather than elapsed time. What must not change is
    // that a duplicate is still dropped, the first occurrence still wins, and
    // order is still source order — a set that replaced the scan but let a
    // later duplicate overwrite an earlier one would be faster and wrong.
    let mut markup = String::from("<div");
    for i in 0..5_000 {
        markup.push_str(&format!(" a{i}='{i}'"));
    }
    // Duplicates of the first and last real attributes, with different values.
    markup.push_str(" a0='late' a4999='late'>");

    let result = turing_html::Tokenizer::new(&markup)
        .tokenize()
        .expect("tokenizes");

    let turing_html::Token::StartTag { attributes, .. } = &result.tokens[0] else {
        panic!("expected a start tag");
    };
    assert_eq!(
        attributes.len(),
        5_000,
        "duplicates dropped, originals kept"
    );
    assert_eq!(attributes[0].name, "a0", "source order preserved");
    assert_eq!(attributes[0].value, "0", "the first occurrence wins");
    assert_eq!(attributes[4_999].value, "4999");
    assert_eq!(
        result
            .errors
            .iter()
            .filter(|e| e.kind == turing_html::ParseErrorKind::DuplicateAttribute)
            .count(),
        2,
        "both duplicates reported"
    );
}

// -- accessible name size ------------------------------------------------

/// Builds `depth` nested links, each carrying `text`.
///
/// Nesting name-from-content roles is what multiplies a document's own text:
/// every link re-collects everything below it.
fn nested_links(depth: usize, text: &str) -> String {
    let open: String = (0..depth).map(|_| format!("<a href='#'>{text}")).collect();
    format!("<html><body>{open}{}</body></html>", "</a>".repeat(depth))
}

#[test]
fn an_oversized_accessible_name_is_refused_rather_than_truncated() {
    // Truncating would hand an assistive technology a name that reads as
    // complete, which is a worse failure than refusing: the user has no signal
    // that anything was dropped.
    let markup = nested_links(200, &"word ".repeat(200));
    let document = document_of(&markup);
    assert!(matches!(
        turing_a11y::build(&document),
        Err(turing_a11y::A11yError::NameTooLong { .. })
    ));
}

#[test]
fn a_single_enormous_text_node_is_refused() {
    // The limit must sit on accumulation generally, not only on the
    // concatenation path that nesting exercises. One huge text node inside one
    // link reaches it without any nesting at all.
    let huge = "x".repeat(turing_a11y::MAX_ACCESSIBLE_NAME_BYTES + 1);
    let document = document_of(&format!("<html><body><a href='#'>{huge}</a></body></html>"));
    assert!(matches!(
        turing_a11y::build(&document),
        Err(turing_a11y::A11yError::NameTooLong { .. })
    ));
}

#[test]
fn a_labelledby_target_is_bounded_too() {
    // aria-labelledby resolves its targets through the same collection, so a
    // bound applied only to name-from-content would leave this path open.
    let huge = "x".repeat(turing_a11y::MAX_ACCESSIBLE_NAME_BYTES + 1);
    let document = document_of(&format!(
        "<html><body><span id='big'>{huge}</span>\
         <button aria-labelledby='big'></button></body></html>"
    ));
    assert!(matches!(
        turing_a11y::build(&document),
        Err(turing_a11y::A11yError::NameTooLong { .. })
    ));
}

#[test]
fn ordinary_names_are_unaffected() {
    // A bound that refused real documents would be a regression dressed as a
    // fix. Real accessible names are a handful of words.
    let document = document_of(&nested_links(20, "Read more"));
    let tree = turing_a11y::build(&document).expect("builds");

    fn first_name(node: &turing_a11y::AccessibilityNode) -> Option<String> {
        node.name
            .clone()
            .or_else(|| node.children.iter().find_map(first_name))
    }
    assert!(
        first_name(&tree).is_some_and(|name| name.contains("Read more")),
        "a normal nested name still resolves"
    );
}

#[test]
fn name_growth_stays_within_the_documented_bound() {
    // The composite bound is depth times the per-name limit. Asserted on the
    // produced sizes rather than on elapsed time, so it cannot fail for reasons
    // unrelated to the code.
    fn name_bytes(node: &turing_a11y::AccessibilityNode) -> usize {
        node.name.as_ref().map_or(0, String::len)
            + node.children.iter().map(name_bytes).sum::<usize>()
    }

    let document = document_of(&nested_links(200, "word"));
    let tree = turing_a11y::build(&document).expect("builds");
    let produced = name_bytes(&tree);
    let ceiling = turing_a11y::MAX_ACCESSIBLE_NAME_BYTES * turing_a11y::MAX_NESTING_DEPTH;
    assert!(
        produced <= ceiling,
        "produced {produced} bytes of names, above the documented ceiling {ceiling}"
    );
}

// -- script execution budgets --------------------------------------------

#[test]
fn repeated_doubling_is_refused_rather_than_allocated() {
    // The step limit bounds how many operations run, not how much each one
    // allocates. `s = s + s` doubles its result every iteration, so twenty-seven
    // iterations — a rounding error against a million-step budget — produced two
    // gigabytes from a hundred-byte script, in seven seconds.
    let source = "let s = 'aaaaaaaaaaaaaaaa'; let i = 0; \
                  while (i < 27) { s = s + s; i = i + 1; } s";
    assert!(matches!(
        turing_js::evaluate(source),
        Err(turing_js::JsError::ByteLimitExceeded { .. })
    ));
}

#[test]
fn the_byte_budget_is_reached_long_before_the_step_budget() {
    // The two budgets bound different things, and this is the case that shows
    // it: a script well inside the step limit must still be stopped. If this
    // ever reports StepLimitExceeded instead, the byte budget has stopped
    // doing the work it was added for.
    let source = "let s = 'aaaaaaaaaaaaaaaa'; let i = 0; \
                  while (i < 40) { s = s + s; i = i + 1; } s";
    match turing_js::evaluate(source) {
        Err(turing_js::JsError::ByteLimitExceeded { .. }) => {}
        other => panic!("expected the byte budget to stop this, got {other:?}"),
    }
}

#[test]
fn the_budget_brackets_where_it_should() {
    // The pair that proves the counting is real rather than incidental. Each
    // iteration concatenates two thirty-byte strings, so it charges sixty
    // bytes: sixteen thousand iterations stay under the million-byte budget and
    // seventeen thousand pass it.
    //
    // Asserted on acceptance and refusal rather than on a returned value,
    // because `evaluate` discards the top level's completion value by design —
    // an external caller cannot observe a script's result at all.
    let loop_of = |iterations: u32| {
        format!(
            "function main() {{ let t = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';              let s = ''; let i = 0;              while (i < {iterations}) {{ s = t + t; i = i + 1; }} return s; }} main();"
        )
    };

    assert!(
        turing_js::evaluate(&loop_of(16_000)).is_ok(),
        "960,000 bytes is inside the budget"
    );
    assert!(
        matches!(
            turing_js::evaluate(&loop_of(17_000)),
            Err(turing_js::JsError::ByteLimitExceeded { .. })
        ),
        "1,020,000 bytes is outside it"
    );
}

#[test]
fn ordinary_string_building_is_unaffected() {
    // A budget that refused real scripts would be a regression dressed as a
    // fix. Building half a kilobyte a piece at a time is ordinary work.
    let source = "function main() { let s = ''; let i = 0;                   while (i < 100) { s = s + 'chunk'; i = i + 1; } return s; } main();";
    assert!(turing_js::evaluate(source).is_ok());
}

#[test]
fn assigning_a_literal_repeatedly_is_not_charged() {
    // Only concatenation amplifies. Copying a literal leaves one live value
    // however many times it happens, so charging it would refuse ordinary loops
    // for no safety gain — the step limit already bounds the churn.
    //
    // Sized so the point is provable: fifty thousand copies of a thirty-byte
    // literal would be 1.5 MB against a 1 MB budget if copies were charged, and
    // the loop stays well inside the step limit so that budget is not what
    // decides the outcome.
    //
    // Recorded because two earlier versions of this test were wrong — one
    // assumed literal assignment was charged, the other ran long enough to hit
    // the step limit and blame the wrong budget.
    let source = "function main() { let t = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';                   let s = ''; let i = 0;                   while (i < 50000) { s = t; i = i + 1; } return s; } main();";
    assert!(turing_js::evaluate(source).is_ok());
}
