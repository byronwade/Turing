// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Script mutating the document, and what that invalidates.
//!
//! These tests span four crates on purpose. Each one behaves correctly alone —
//! the DOM advances its epoch, the router checks one — and the property that
//! matters only exists where they meet: a script changing the page must make
//! stale geometry unusable rather than merely different.

use turing_dom::{Dom, Event};
use turing_html::{Tokenizer, TreeBuilder};
use turing_input::{HitRouter, InputError};
use turing_js::{Host, JsError, Value, Vm, compile};
use turing_layout::{LayoutBox, Point, TextMetrics, layout};
use turing_webidl::DomHost;

const PAGE: &str = "<html><body><div id='panel' class='card'>text</div></body></html>";
const SHEET: &str = "body { display: block; } #panel { display: block; height: 30px; }";

fn dom() -> Dom {
    let tokens = Tokenizer::new(PAGE).tokenize().expect("tokenizes").tokens;
    Dom::new(TreeBuilder::new().build(&tokens).expect("builds"))
}

fn layout_of(dom: &Dom) -> LayoutBox {
    let sheet = turing_css::Stylesheet::parse(SHEET).expect("parses");
    layout(dom.document(), &sheet, 400.0, TextMetrics::default()).expect("lays out")
}

/// Runs `body` as the whole of `main` against `host`.
fn run(host: &mut dyn Host, body: &str) -> Result<Value, JsError> {
    let program = compile(&format!("function main() {{ {body} }}")).expect("compiles");
    Vm::default().call(&program, "main", Vec::new(), host)
}

// -- mutation ------------------------------------------------------------

#[test]
fn script_changes_an_attribute_and_the_document_reflects_it() {
    let mut dom = dom();
    let mut host = DomHost::new(&mut dom);

    run(&mut host, "setAttribute('panel', 'class', 'changed');").expect("runs");

    assert_eq!(
        run(&mut host, "return getAttribute('panel', 'class');").expect("runs"),
        Value::String("changed".to_string())
    );
}

#[test]
fn script_removes_an_attribute() {
    let mut dom = dom();
    let mut host = DomHost::new(&mut dom);

    run(&mut host, "removeAttribute('panel', 'class');").expect("runs");

    assert_eq!(
        run(&mut host, "return getAttribute('panel', 'class');").expect("runs"),
        Value::Null
    );
}

// -- invalidation --------------------------------------------------------

#[test]
fn a_script_mutation_invalidates_layout_computed_before_it() {
    // The property these crates only have together. A router built against the
    // page as it was must refuse after script changes the page, rather than
    // routing a click using geometry that no longer describes it.
    let mut dom = dom();
    let router = HitRouter::new(&dom, layout_of(&dom));
    let point = Point { x: 10.0, y: 10.0 };

    // Routing works before the script runs.
    assert!(router.target_at(&dom, point).is_ok());

    let mut host = DomHost::new(&mut dom);
    run(&mut host, "setAttribute('panel', 'class', 'changed');").expect("runs");
    drop(host);

    assert!(matches!(
        router.dispatch_at(&dom, point, &Event::new("click")),
        Err(InputError::LayoutOutOfDate { .. })
    ));
}

#[test]
fn a_script_that_only_reads_leaves_layout_usable() {
    // The other side of the bracket. If reads invalidated too, every script
    // would force a relayout and the check would be worthless as a signal.
    let mut dom = dom();
    let router = HitRouter::new(&dom, layout_of(&dom));
    let point = Point { x: 10.0, y: 10.0 };

    let mut host = DomHost::new(&mut dom);
    run(&mut host, "return tagName('panel');").expect("runs");
    run(&mut host, "return textContent('panel');").expect("runs");
    drop(host);

    assert!(
        router.target_at(&dom, point).is_ok(),
        "reading must not invalidate layout"
    );
}

#[test]
fn a_mutation_refused_by_the_binding_does_not_invalidate_layout() {
    // Load-bearing rather than incidental. If a failed mutation advanced the
    // epoch, a script probing for elements that do not exist would invalidate
    // every cached layout while changing nothing — a denial of service made of
    // typos.
    //
    // This covers refusal at the binding's own lookup, which is where a bad id
    // stops. Refusal *inside* the DOM cannot be reached from here — every id
    // that resolves resolves to an element — so the DOM's own ordering is
    // tested in `turing-dom`, next to the code that has to get it right.
    let mut dom = dom();
    let router = HitRouter::new(&dom, layout_of(&dom));
    let point = Point { x: 10.0, y: 10.0 };

    let mut host = DomHost::new(&mut dom);
    let result = run(&mut host, "setAttribute('absent', 'class', 'x');");
    assert!(
        matches!(result, Err(JsError::HostOperationFailed { .. })),
        "the mutation was refused"
    );
    drop(host);

    assert!(
        router.target_at(&dom, point).is_ok(),
        "a mutation that did not happen must not invalidate anything"
    );
}

// -- restricting the surface ---------------------------------------------

#[test]
fn a_read_only_host_refuses_every_mutating_operation() {
    let mut dom = dom();
    let mut host = DomHost::read_only(&mut dom);

    for call in [
        "setAttribute('panel', 'class', 'x');",
        "removeAttribute('panel', 'class');",
    ] {
        assert!(
            matches!(run(&mut host, call), Err(JsError::UnboundOperation { .. })),
            "{call} must be unbound on a read-only host"
        );
    }
}

#[test]
fn a_read_only_host_still_reads() {
    // A restriction that removed everything would pass the test above and be
    // useless.
    let mut dom = dom();
    let mut host = DomHost::read_only(&mut dom);

    assert_eq!(
        run(&mut host, "return tagName('panel');").expect("runs"),
        Value::String("div".to_string())
    );
}

#[test]
fn a_read_only_host_lists_no_mutating_operation() {
    // The listing and the callable set are the same table, so this is implied —
    // asserted anyway because that equivalence is the registry's whole reason
    // for existing and is worth failing loudly if it ever stops holding.
    let mut dom = dom();
    let host = DomHost::read_only(&mut dom);

    for operation in host.bindings().operations() {
        assert!(
            !operation.name.starts_with("set") && !operation.name.starts_with("remove"),
            "{} is listed on a read-only host",
            operation.name
        );
    }
    assert!(
        !host.bindings().operations().is_empty(),
        "the read-only surface is not empty"
    );
}

#[test]
fn a_read_only_host_cannot_change_the_document() {
    // The behaviour, not just the registry state: a refused call must also
    // leave the document alone.
    let mut dom = dom();
    let mut host = DomHost::read_only(&mut dom);
    let before = host.dom().epoch();

    let _ = run(&mut host, "setAttribute('panel', 'class', 'x');");

    assert_eq!(host.dom().epoch(), before, "the epoch did not move");
    assert_eq!(
        run(&mut host, "return getAttribute('panel', 'class');").expect("runs"),
        Value::String("card".to_string()),
        "the attribute is unchanged"
    );
}
