// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Routing a pointer location to a dispatched DOM event.
//!
//! The cases that matter are the ones where routing produces a plausible wrong
//! answer: a hit against stale geometry, a click on nothing, and propagation
//! reaching the wrong ancestors or in the wrong order.

use turing_dom::{Dom, Event, Phase};
use turing_html::{NodeId, Tokenizer, TreeBuilder};
use turing_input::{HitRouter, InputError};
use turing_layout::{LayoutBox, Point, TextMetrics, layout};

const PAGE: &str = "<html><body><div id='outer'><p id='inner'>hello</p></div></body></html>";
const SHEET: &str = "body { display: block; } \
                     #outer { display: block; height: 60px; } \
                     #inner { display: block; height: 20px; }";

fn dom_of(html: &str) -> Dom {
    let tokens = Tokenizer::new(html).tokenize().expect("tokenizes").tokens;
    Dom::new(TreeBuilder::new().build(&tokens).expect("builds"))
}

fn layout_of(dom: &Dom) -> LayoutBox {
    let sheet = turing_css::Stylesheet::parse(SHEET).expect("parses");
    layout(dom.document(), &sheet, 400.0, TextMetrics::default(), None).expect("lays out")
}

fn node_named(dom: &Dom, id: &str) -> NodeId {
    let document = dom.document();
    (0..document.len())
        .map(NodeId::from_index)
        .find(|&n| document.element_by_id(id) == Some(n))
        .expect("the element exists")
}

/// A point inside the element with the given id.
fn point_in(dom: &Dom, root: &LayoutBox, id: &str) -> Point {
    let target = node_named(dom, id);
    fn walk(node: &LayoutBox, index: usize) -> Option<&LayoutBox> {
        if node.node == Some(index) {
            return Some(node);
        }
        node.children.iter().find_map(|c| walk(c, index))
    }
    let box_for = walk(root, target.index()).expect("the element has a box");
    Point {
        x: box_for.dimensions.content.x + 1.0,
        y: box_for.dimensions.content.y + 1.0,
    }
}

// -- staleness -----------------------------------------------------------

#[test]
fn routing_against_a_changed_document_is_refused() {
    // The failure this crate exists to make visible. A layout box tree is a
    // photograph; once the document moves on, a hit names whichever node used to
    // be at that location. Nothing about this is visible in a test where the
    // document does not change, which is every obvious test.
    let mut dom = dom_of(PAGE);
    let router = HitRouter::new(&dom, layout_of(&dom));
    let point = point_in(&dom, &layout_of(&dom), "inner");

    // Any structural mutation advances the epoch.
    let text = dom.create_text("late arrival");
    let outer = dom.handle(node_named(&dom, "outer"));
    dom.append_child(outer, text).expect("appends");

    assert!(matches!(
        router.dispatch_at(&dom, point, &Event::new("click")),
        Err(InputError::LayoutOutOfDate { .. })
    ));
}

#[test]
fn an_attribute_change_also_invalidates_routing() {
    // Attribute changes advance the epoch because a selector match can depend
    // on one, so geometry can change without the tree's shape changing. Routing
    // must treat that as staleness too.
    let mut dom = dom_of(PAGE);
    let router = HitRouter::new(&dom, layout_of(&dom));
    let point = point_in(&dom, &layout_of(&dom), "inner");

    let inner = dom.handle(node_named(&dom, "inner"));
    dom.set_attribute(inner, "class", "changed")
        .expect("sets the attribute");

    assert!(matches!(
        router.target_at(&dom, point),
        Err(InputError::LayoutOutOfDate { .. })
    ));
}

#[test]
fn an_unchanged_document_routes() {
    // The other side of the bracket. A staleness check that refused everything
    // would pass the test above and be useless.
    let dom = dom_of(PAGE);
    let router = HitRouter::new(&dom, layout_of(&dom));
    let point = point_in(&dom, &layout_of(&dom), "inner");

    assert_eq!(
        router.target_at(&dom, point).expect("routes"),
        Some(node_named(&dom, "inner"))
    );
}

// -- targeting -----------------------------------------------------------

#[test]
fn a_point_over_nothing_dispatches_nothing() {
    // Returning the root would be the tempting default and would deliver events
    // nobody aimed at anything.
    let dom = dom_of(PAGE);
    let router = HitRouter::new(&dom, layout_of(&dom));

    let outcome = router
        .dispatch_at(
            &dom,
            Point {
                x: 10.0,
                y: 9_000.0,
            },
            &Event::new("click"),
        )
        .expect("routes");
    assert!(outcome.is_none());
}

#[test]
fn the_innermost_element_is_the_target() {
    // The paragraph sits inside the div, so both contain the point. Hit testing
    // resolves the topmost; routing must not widen that to an ancestor.
    let dom = dom_of(PAGE);
    let router = HitRouter::new(&dom, layout_of(&dom));
    let point = point_in(&dom, &layout_of(&dom), "inner");

    assert_eq!(
        router.target_at(&dom, point).expect("routes"),
        Some(node_named(&dom, "inner"))
    );
}

// -- propagation ---------------------------------------------------------

#[test]
fn a_click_propagates_through_the_ancestors_in_order() {
    // End to end: a point becomes a target, and the target's ancestors see the
    // event in capture order then bubble order. Routing that delivered to the
    // right node but bypassed propagation would pass every targeting test here.
    let mut dom = dom_of(PAGE);
    let outer = dom.handle(node_named(&dom, "outer"));
    let inner = dom.handle(node_named(&dom, "inner"));

    dom.add_listener(outer, "click", "outer-capture", true, &[])
        .expect("registers");
    dom.add_listener(inner, "click", "inner-bubble", false, &[])
        .expect("registers");
    dom.add_listener(outer, "click", "outer-bubble", false, &[])
        .expect("registers");

    let router = HitRouter::new(&dom, layout_of(&dom));
    let point = point_in(&dom, &layout_of(&dom), "inner");

    let dispatch = router
        .dispatch_at(&dom, point, &Event::new("click"))
        .expect("routes")
        .expect("something was hit");

    let order: Vec<_> = dispatch
        .invocations
        .iter()
        .map(|invocation| (invocation.node, invocation.phase))
        .collect();
    assert_eq!(
        order,
        vec![
            (outer.node(), Phase::Capturing),
            (inner.node(), Phase::AtTarget),
            (outer.node(), Phase::Bubbling),
        ],
        "capture runs outermost first, bubble innermost first"
    );
}

#[test]
fn registering_a_listener_does_not_invalidate_routing() {
    // Listener registration deliberately does not advance the epoch: it changes
    // nothing a selector can match and nothing layout depends on. If it did,
    // attaching a handler would break the router that is about to use it, which
    // is exactly the order a real page does things in.
    let mut dom = dom_of(PAGE);
    let router = HitRouter::new(&dom, layout_of(&dom));
    let point = point_in(&dom, &layout_of(&dom), "inner");

    let inner = dom.handle(node_named(&dom, "inner"));
    dom.add_listener(inner, "click", "handler", false, &[])
        .expect("registers");

    let dispatch = router
        .dispatch_at(&dom, point, &Event::new("click"))
        .expect("routing still works after attaching a listener")
        .expect("something was hit");
    assert_eq!(dispatch.invocations.len(), 1);
}
