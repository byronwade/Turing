// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! A concrete answer to "can the engine render the browser's own chrome,
//! instead of hand-written Rust widgets": `nova_chrome_demo.html` is
//! ordinary HTML/CSS/JS describing a tab strip and an address/search pill,
//! styled with colours and dimensions taken directly from
//! `design/tokens.json` (the machine-readable extraction of the hash-pinned
//! Nova design source). This file loads it through `turing_engine::Page` —
//! the same load/render/dispatch API any embedder uses — clicks a tab, and
//! confirms the active tab actually changed, through the real DOM/CSS/paint
//! pipeline, not a mock.
//!
//! Run with `cargo run -p turing-engine --example nova_chrome_demo`.
//!
//! # What this does and does not prove
//!
//! It proves the engine can paint this UI from real markup and respond to a
//! real click by mutating the DOM and repainting — the same loop
//! `apps/turing-browser` already uses for page content. It does **not**
//! prove this replaces `turing-chrome` as the browser's actual trusted
//! chrome: that specific substitution is exactly what `ADR-0008`
//! (`docs/blueprint-v1/17-architecture-decisions.md`) and the product
//! charter gate behind a security review, because an address bar rendered
//! by the same engine that renders untrusted page content is a real
//! trust-boundary question, not just an implementation detail. See
//! `docs/application-runtime/README.md`'s milestone ladder (APP-6/APP-7) for
//! what still has to be true before that boundary can be revisited.
//!
//! # A layout limitation this fixture worked around
//!
//! Nothing in `turing-layout` currently threads an inline child's own
//! `margin` into how far the next sibling's pen position advances — only
//! `inline_advance_width` (content plus padding) does. A `margin` on a
//! `display: inline` element therefore does not create a gap before the
//! next inline sibling; only a genuine, non-whitespace-only text run
//! between them does (a text node that is *only* whitespace is discarded at
//! box-generation before layout ever sees it, so an empty `<span> </span>`
//! spacer does not work either). This fixture separates its tabs with a
//! literal `.` character rather than CSS spacing for exactly that reason —
//! a real, undocumented-until-now gap, not a mistake in this file.

use turing_dom::Event;
use turing_engine::Page;
use turing_layout::Point;

fn main() {
    let html = include_str!("nova_chrome_demo.html");
    let mut page = Page::load(html, 500.0).expect("the fixture is well-formed");

    println!("title: {:?}", page.title());

    // A point inside "Nova Design"'s own tab box, in the word-gap between
    // "Nova" and "Design" rather than on either glyph — sampling on
    // rendered text reads the label's foreground colour, not the tab's
    // background, the exact trap
    // `docs/embedding/using-turing-engine-today.md` documents.
    let tab1_click_point = Point { x: 141.0, y: 15.0 };
    let target = page
        .target_at(tab1_click_point)
        .expect("routes")
        .expect("the point lands on a tab");
    let target_id = page.dom().document().attribute_of(target, "id");
    println!("point resolves to element id={target_id:?}");
    assert_eq!(
        target_id,
        Some("tab1"),
        "the click point must land on the Nova Design tab, not a neighbour"
    );

    let before = page.render(500, 60).expect("canvas within the size limit");
    let before_pixel = before.pixel(141, 15);
    println!("pixel under tab1's own background before the click: {before_pixel:?}");

    let dispatch = page
        .dispatch_at(tab1_click_point, &Event::new("click"))
        .expect("dispatch succeeds")
        .expect("the click hit tab1");
    println!(
        "listeners the dispatch ran: {:?}",
        dispatch
            .invocations
            .iter()
            .map(|invocation| invocation.listener.as_str())
            .collect::<Vec<_>>()
    );

    let after = page.render(500, 60).expect("canvas within the size limit");
    let after_pixel = after.pixel(141, 15);
    println!("pixel under tab1's own background after the click: {after_pixel:?}");
    assert_ne!(
        before_pixel, after_pixel,
        "clicking a tab must visibly move the active-tab background, through \
         real setAttribute + relayout + repaint, not a hardcoded Rust widget"
    );
    println!(
        "the engine rendered this chrome from HTML/CSS and the click genuinely \
         switched the active tab through the real DOM/CSS/paint pipeline."
    );
}
