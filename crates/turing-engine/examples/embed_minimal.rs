// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! The minimal embedding walkthrough: everything a third-party program needs
//! from `turing-engine` as a library, in one file.
//!
//! Run with `cargo run -p turing-engine --example embed_minimal`. It takes no
//! arguments and writes nothing to disk — it is meant to be read, not just
//! run, alongside `docs/embedding/using-turing-engine-today.md`, which walks
//! through it line by line.
//!
//! `render_page` (the other example in this directory) is the reproducible
//! headless-screenshot tool this workspace's own tests and demos use. This
//! file is different on purpose: it exercises the *interactive* half of the
//! API — a script-registered listener, a simulated click, and the DOM
//! mutation and repaint that follow — because "load a page and draw it" is
//! only half of what embedding this engine actually means.

use turing_engine::Page;

fn main() {
    // A page with a button and a script that flips its own text and colour
    // when clicked. No network, no file — the HTML string is the whole
    // input, exactly as it would be for a program that generates or receives
    // its own markup.
    let html = "<html><head><title>Embedding demo</title><style>\
        .off { background: firebrick; color: white; }\
        .on { background: forestgreen; color: white; }\
        </style></head>\
        <body>\
        <div id='button' class='off'>Click me</div>\
        <script>\
        function flip() { setAttribute('button', 'class', 'on'); }\
        addEventListener('button', 'click', 'flip');\
        </script>\
        </body></html>";

    // `Page::load` parses, cascades, runs every `<script>` once against the
    // live document, and lays out — one call, one `Result`, no separate
    // "now render" step required before the page is usable.
    let mut page = Page::load(html, 320.0).expect("the demo page is well-formed");

    println!("title: {:?}", page.title());
    println!("content height: {}px", page.content_height());

    // `render` rasterises the current layout onto a canvas of the given
    // pixel size. A canvas is a plain sRGB pixel buffer — `Canvas::pixel`
    // reads one pixel back, which is enough to prove the click below
    // actually changed what paints, without needing to save a file.
    //
    // The sample point is (200, 5): the button spans the full 320px width
    // but its label text ("Click me", drawn in the foreground colour) only
    // occupies the left ~64px in the 8x8 bitmap font, so a point further
    // right samples the div's background fill rather than a glyph stroke.
    let before = page.render(320, 60).expect("canvas within the size limit");
    let before_pixel = before.pixel(200, 5);
    println!("pixel under the button before the click: {before_pixel:?}");

    // `target_at` answers "what element is at this point" against the live,
    // laid-out page — the same query a real input pipeline would run before
    // deciding what to dispatch to.
    let point = turing_layout::Point { x: 200.0, y: 5.0 };
    let hit = page
        .target_at(point)
        .expect("routing succeeds")
        .expect("the point lands on the button");
    let hit_id = page.dom().document().attribute_of(hit, "id");
    println!("element under the point: id={hit_id:?}");

    // `dispatch_at` is the whole interactive loop in one call: it routes the
    // event through capture/target/bubble, runs whatever script listeners
    // the dispatch reports (in that order, against the live document), and
    // re-lays out if anything mutated — a caller never has to remember to
    // call layout again after a click.
    let dispatch = page
        .dispatch_at(point, &turing_dom::Event::new("click"))
        .expect("dispatch succeeds")
        .expect("the click hit the button");
    println!(
        "listeners the dispatch ran: {:?}",
        dispatch
            .invocations
            .iter()
            .map(|invocation| invocation.listener.as_str())
            .collect::<Vec<_>>()
    );

    // The mutation is already visible in a fresh render — no extra "commit"
    // or "flush" step, because `dispatch_at` already relaid out.
    let after = page.render(320, 60).expect("canvas within the size limit");
    let after_pixel = after.pixel(200, 5);
    println!("pixel under the button after the click: {after_pixel:?}");
    assert_ne!(
        before_pixel, after_pixel,
        "the click's script mutation must be visible in the very next render"
    );
    println!("the click's DOM mutation is visible in the next render.");
}
