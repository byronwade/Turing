// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! End-to-end tests: HTML source in, pixels and routed events out.

use turing_css::Color;
use turing_dom::Event;
use turing_engine::{EngineError, Page};
use turing_layout::Point;

fn color(name: &str) -> Color {
    Color::parse(name).expect("parses")
}

const PAGE: &str = "<html><head><title>Lab Page</title>\
    <style>body { background: white; } #banner { background: navy; color: white; }</style>\
    </head><body><div id='banner'>Turing</div></body></html>";

#[test]
fn a_page_renders_its_background_and_its_text() {
    let page = Page::load(PAGE, 320.0).expect("loads");
    let canvas = page.render(320, 64).expect("renders");

    // The banner block spans the viewport width and one 16px line.
    assert_eq!(canvas.pixel(300, 8), Some(color("navy")), "banner fill");
    // "Turing" starts at the content origin: 'T' row 0 is 0x3F, so the
    // top-left of the first glyph cell has ink at x = 0, y = 4.
    assert_eq!(
        canvas.pixel(0, 4),
        Some(color("white")),
        "glyph ink over navy"
    );
    // Below the banner the canvas is untouched background.
    assert_eq!(
        canvas.pixel(300, 40),
        Some(color("white")),
        "canvas background"
    );
}

#[test]
fn the_title_comes_from_the_title_element() {
    let page = Page::load(PAGE, 320.0).expect("loads");
    assert_eq!(page.title().as_deref(), Some("Lab Page"));
    let untitled = Page::load("<html><body>x</body></html>", 320.0).expect("loads");
    assert_eq!(untitled.title(), None);
}

#[test]
fn a_load_time_script_mutation_is_visible_in_the_first_layout() {
    // The script rewrites the element's class before first layout, so the
    // wide rule applies from the start — the page never renders un-mutated.
    let html = "<html><head><style>\
        .before { background: red; } .after { background: lime; }\
        </style></head><body><div id='box' class='before'>x</div>\
        <script>setAttribute('box', 'class', 'after');</script></body></html>";
    let page = Page::load(html, 100.0).expect("loads");
    let canvas = page.render(100, 32).expect("renders");
    assert_eq!(
        canvas.pixel(50, 8),
        Some(color("lime")),
        "script won before paint"
    );
}

#[test]
fn a_script_syntax_refusal_fails_the_load_rather_than_half_loading() {
    let html = "<html><body><script>class X {}</script></body></html>";
    let result = Page::load(html, 100.0);
    assert!(
        matches!(result, Err(EngineError::Script(_))),
        "unsupported syntax must refuse the load, got {result:?}"
    );
}

#[test]
fn a_click_routes_to_the_element_under_the_point() {
    let page = Page::load(PAGE, 320.0).expect("loads");
    let target = page
        .target_at(Point { x: 4.0, y: 8.0 })
        .expect("routes")
        .expect("hits");
    assert_eq!(
        page.dom().document().attribute_of(target, "id"),
        Some("banner"),
        "the point inside the banner resolves to the banner"
    );
}

#[test]
fn dispatch_reaches_listeners_through_the_live_document() {
    let mut page = Page::load(PAGE, 320.0).expect("loads");
    let dispatch = page
        .dispatch_at(Point { x: 4.0, y: 8.0 }, &Event::new("click"))
        .expect("dispatches")
        .expect("hit something");
    // No listeners are registered, so the dispatch record is empty — the
    // point is that the full route (hit test, handle mint, three-phase walk)
    // ran without a staleness refusal.
    assert!(dispatch.invocations.is_empty());
}

#[test]
fn a_post_load_script_mutation_relays_out_before_the_next_query() {
    // Swapping the banner's class to a rule that hides it means the next hit
    // test must miss. If the page did not re-lay out, the router would either
    // refuse (stale epoch) or hit stale geometry; both would fail this test.
    let html = "<html><head><style>\
        #banner { background: navy; } .gone { display: none; }\
        </style></head><body><div id='banner'>Turing</div></body></html>";
    let mut page = Page::load(html, 320.0).expect("loads");
    assert!(
        page.target_at(Point { x: 4.0, y: 8.0 })
            .expect("routes")
            .is_some(),
        "the banner is hittable before the mutation"
    );

    page.run_script("setAttribute('banner', 'class', 'gone');")
        .expect("runs");

    assert!(
        page.target_at(Point { x: 4.0, y: 8.0 })
            .expect("routes after relayout")
            .is_none(),
        "a display:none element must not be hit"
    );
}

#[test]
fn resizing_reflows_text_onto_more_lines() {
    // Two words that fit one 200px line but not one 60px line.
    let html = "<html><body><span>hello</span> <span>world</span></body></html>";
    let mut page = Page::load(html, 200.0).expect("loads");
    let wide = page.layout().dimensions.content.height;
    page.resize(60.0).expect("resizes");
    let narrow = page.layout().dimensions.content.height;
    assert!(
        narrow > wide,
        "narrowing the viewport must add a line: {wide} -> {narrow}"
    );
}

#[test]
fn a_script_builds_a_dom_subtree_that_lays_out_and_paints() {
    // The application-runtime shape in miniature: script constructs nodes the
    // way a framework renderer does — createElement, setNodeAttribute,
    // createText, appendChild — and the engine lays out and paints the
    // result. Nothing in the source HTML has the built content; it exists
    // only because the script ran.
    let html = "<html><head><style>\
        body { background: white; } .built { background: teal; color: white; }\
        </style></head><body></body>\
        <script>\
        function build() {\
          let root = documentBody();\
          let card = createElement('div');\
          setNodeAttribute(card, 'class', 'built');\
          let text = createText('Made by JS');\
          appendChild(card, text);\
          appendChild(root, card);\
        }\
        build();\
        </script></body></html>";
    let page = Page::load(html, 200.0).expect("loads");

    // The built div paints its teal background — proof the script-created
    // node reached layout and paint.
    let canvas = page.render(200, 32).expect("renders");
    assert_eq!(
        canvas.pixel(100, 8),
        Some(color("teal")),
        "the JS-built card painted its background"
    );
    // Its text is in the display list.
    assert!(
        page.display_list().items.iter().any(|item| matches!(
            item,
            turing_layout::DisplayItem::Text { text, .. } if text.contains("Made")
        )),
        "the JS-built text node is painted"
    );
}

#[test]
fn a_component_runtime_written_in_the_engine_subset_renders() {
    // The application-runtime thesis in miniature: a React-like runtime —
    // virtual nodes via h()/txt(), a recursive render(), and components that
    // are closures capturing const props — written entirely in the engine's
    // own JavaScript subset, producing real DOM the engine lays out and
    // paints. This composes arrays, closures, recursion, and DOM construction.
    let html = "<html><head><style>\
        .card { background: teal; } .badge { background: navy; }\
        </style></head><body></body>\
        <script>\
        function h(tag, cls) { return { tag: tag, cls: cls, kids: [] }; }\
        function txt(s) { return { tag: '#text', text: s }; }\
        function child(p, c) { p.kids[p.kids.length] = c; return p; }\
        function render(v) {\
          if (v.tag === '#text') { return createText(v.text); }\
          let node = createElement(v.tag);\
          if (v.cls) { setNodeAttribute(node, 'class', v.cls); }\
          let i = 0;\
          while (i < v.kids.length) { appendChild(node, render(v.kids[i])); i = i + 1; }\
          return node;\
        }\
        function Card(t) { const title = t; return function() { return child(h('div', 'card'), txt(title)); }; }\
        function main() {\
          let root = h('div', 'app');\
          let items = [Card('one'), Card('two')];\
          let i = 0;\
          while (i < items.length) { let c = items[i]; child(root, c()); i = i + 1; }\
          child(root, child(h('div', 'badge'), txt('done')));\
          appendChild(documentBody(), render(root));\
        }\
        main();\
        </script></body></html>";
    let page = Page::load(html, 200.0).expect("loads");
    let list = page.display_list();
    // Two teal cards and one navy badge were produced by the runtime.
    let teal = list
        .items
        .iter()
        .filter(|item| matches!(item, turing_layout::DisplayItem::SolidColor { color: c, .. } if *c == color("teal")))
        .count();
    assert_eq!(teal, 2, "two Card components rendered");
    assert!(
        list.items.iter().any(|item| matches!(item, turing_layout::DisplayItem::SolidColor { color: c, .. } if *c == color("navy"))),
        "the badge rendered"
    );
    // The closure-captured const title text is present.
    assert!(
        list.items.iter().any(|item| matches!(item, turing_layout::DisplayItem::Text { text, .. } if text.contains("one"))),
        "a component's captured-const title painted"
    );
}

#[test]
fn a_script_removes_and_reorders_nodes_the_way_a_reconciler_patches() {
    // Mount two rows, then patch: remove the first, read parentNode and
    // firstChild to navigate, and insert a new row before what is now first.
    // The final order is what a reconciler would produce, and it renders.
    let html = "<html><head><style>\
        .a { background: red; } .b { background: lime; } .c { background: blue; }\
        </style></head><body></body>\
        <script>\
        function main() {\
          let root = documentBody();\
          let first = createElement('div');\
          setNodeAttribute(first, 'class', 'a');\
          appendChild(first, createText('first'));\
          appendChild(root, first);\
          let second = createElement('div');\
          setNodeAttribute(second, 'class', 'b');\
          appendChild(second, createText('second'));\
          appendChild(root, second);\
          removeChild(first);\
          let fresh = createElement('div');\
          setNodeAttribute(fresh, 'class', 'c');\
          appendChild(fresh, createText('fresh'));\
          insertBefore(root, fresh, firstChild(root));\
        }\
        main();\
        </script></body></html>";
    let page = Page::load(html, 200.0).expect("loads");

    // Order is now [fresh (blue), second (lime)] — 'first' (red) is gone.
    let canvas = page.render(200, 48).expect("renders");
    assert_eq!(
        canvas.pixel(100, 8),
        Some(color("blue")),
        "fresh row is first"
    );
    assert_eq!(
        canvas.pixel(100, 24),
        Some(color("lime")),
        "second row follows"
    );
    // No red anywhere: the removed node does not paint.
    let has_red = (0..48).any(|y| canvas.pixel(100, y) == Some(color("red")));
    assert!(!has_red, "the removed node is gone");
}

#[test]
fn a_click_runs_the_script_listener_and_repaints() {
    // The full interactive loop: script registers a listener at load, a
    // dispatched click reports the invocation, the engine calls the named
    // function, the function mutates the DOM, layout re-runs, and the next
    // paint shows the change.
    let html = "<html><head><style>\
        .off { background: red; } .on { background: lime; }\
        </style></head><body><div id='box' class='off'>toggle</div>\
        <script>\
        function flip() { setAttribute('box', 'class', 'on'); }\
        addEventListener('box', 'click', 'flip');\
        </script></body></html>";
    let mut page = Page::load(html, 100.0).expect("loads");
    assert_eq!(
        page.render(100, 32).expect("renders").pixel(50, 8),
        Some(color("red")),
        "before the click the box is red"
    );

    let dispatch = page
        .dispatch_at(Point { x: 4.0, y: 8.0 }, &Event::new("click"))
        .expect("dispatches")
        .expect("hits the box");
    assert_eq!(dispatch.invocations.len(), 1, "the listener ran once");
    assert_eq!(dispatch.invocations[0].listener, "flip");

    assert_eq!(
        page.render(100, 32).expect("renders").pixel(50, 8),
        Some(color("lime")),
        "the click's mutation is visible in the next paint"
    );
}

#[test]
fn a_listener_receives_the_event_kind_and_target_per_its_arity() {
    // The two-parameter listener writes both arguments where the page can
    // show them: the kind becomes the class, the target id an attribute.
    let html = "<html><head><style>.click { background: lime; }</style></head>\
        <body><div id='box'>x</div>\
        <script>\
        function on(kind, target) {\
          setAttribute('box', 'class', kind);\
          setAttribute('box', 'from', target);\
        }\
        addEventListener('box', 'click', 'on');\
        </script></body></html>";
    let mut page = Page::load(html, 100.0).expect("loads");
    page.dispatch_at(Point { x: 4.0, y: 8.0 }, &Event::new("click"))
        .expect("dispatches")
        .expect("hits");
    let target = page
        .target_at(Point { x: 4.0, y: 8.0 })
        .expect("routes")
        .expect("still hittable");
    let document = page.dom().document();
    assert_eq!(document.attribute_of(target, "class"), Some("click"));
    assert_eq!(document.attribute_of(target, "from"), Some("box"));
}

#[test]
fn a_listener_naming_a_missing_function_is_a_script_error() {
    let html = "<html><body><div id='box'>x</div>\
        <script>addEventListener('box', 'click', 'ghost');</script></body></html>";
    let mut page = Page::load(html, 100.0).expect("loads");
    let result = page.dispatch_at(Point { x: 4.0, y: 8.0 }, &Event::new("click"));
    assert!(
        matches!(result, Err(EngineError::Script(_))),
        "a registered-but-undefined listener must refuse, got {result:?}"
    );
}

#[test]
fn a_function_defined_by_run_script_is_callable_from_a_listener() {
    let html = "<html><head><style>.on { background: lime; }</style></head>\
        <body><div id='box'>x</div></body></html>";
    let mut page = Page::load(html, 100.0).expect("loads");
    page.run_script(
        "function arm() { setAttribute('box', 'class', 'on'); }\
         addEventListener('box', 'click', 'arm');",
    )
    .expect("runs");
    page.dispatch_at(Point { x: 4.0, y: 8.0 }, &Event::new("click"))
        .expect("dispatches")
        .expect("hits");
    assert_eq!(
        page.render(100, 32).expect("renders").pixel(50, 8),
        Some(color("lime"))
    );
}

#[test]
fn scrolling_translates_paint_without_touching_geometry() {
    let page = Page::load(PAGE, 320.0).expect("loads");
    let scrolled = page.render_scrolled(320, 64, 8.0).expect("renders");
    let unscrolled = page.render(320, 64).expect("renders");

    // The banner pixel that sat at y = 8 is at y = 0 after scrolling 8.
    assert_eq!(
        scrolled.pixel(300, 0),
        unscrolled.pixel(300, 8),
        "paint shifted up"
    );
    // Geometry is untouched: the same page point still hits the banner.
    let target = page
        .target_at(Point { x: 4.0, y: 8.0 })
        .expect("routes")
        .expect("hits");
    assert_eq!(
        page.dom().document().attribute_of(target, "id"),
        Some("banner")
    );
    // The content height is the page's, not the window's.
    assert!(page.content_height() >= 16.0);
}

#[test]
fn an_unsupported_stylesheet_notation_refuses_the_load() {
    // The colour is validated where style is resolved, so the refusal
    // arrives from the layout stage wearing the CSS value error. lab() is
    // the example now that rgb() and hsl() both parse.
    let html = "<html><head><style>body { background: lab(50% 40 59.5); }</style>\
        </head><body>x</body></html>";
    assert!(matches!(
        Page::load(html, 100.0),
        Err(EngineError::Layout(_))
    ));
}
