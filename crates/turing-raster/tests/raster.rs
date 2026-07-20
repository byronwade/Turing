// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Reference rasterizer tests.
//!
//! The display lists here are built by hand rather than produced by layout.
//! That is deliberate: it proves the rasterizer consumes the display list as a
//! contract, independent of how the list was made, which is the property an
//! embedder relies on when they drive it from their own painter pipeline.

use turing_css::Color;
use turing_layout::{DisplayItem, DisplayList, Rect};
use turing_raster::{Canvas, MAX_PIXELS, RasterError, rasterize};

fn color(name: &str) -> Color {
    Color::parse(name).expect("a named colour in the modelled set")
}

fn rect(x: f32, y: f32, width: f32, height: f32) -> Rect {
    Rect {
        x,
        y,
        width,
        height,
    }
}

fn list(items: Vec<DisplayItem>) -> DisplayList {
    DisplayList { items }
}

fn fill(x: f32, y: f32, width: f32, height: f32, name: &str) -> DisplayItem {
    DisplayItem::SolidColor {
        rect: rect(x, y, width, height),
        color: color(name),
    }
}

// -- coverage ------------------------------------------------------------

#[test]
fn coverage_is_half_open() {
    // A rect at x = 0 with width = 2 covers columns 0 and 1, not 0 through 2.
    // A closed interval makes every fill one pixel too wide, which no
    // single-box test notices and which makes adjacent boxes overlap.
    let canvas = rasterize(
        &list(vec![fill(0.0, 0.0, 2.0, 2.0, "red")]),
        4,
        4,
        color("white"),
    )
    .expect("rasterizes");

    assert_eq!(canvas.pixel(0, 0), Some(color("red")));
    assert_eq!(canvas.pixel(1, 1), Some(color("red")));
    assert_eq!(
        canvas.pixel(2, 0),
        Some(color("white")),
        "column 2 is outside"
    );
    assert_eq!(canvas.pixel(0, 2), Some(color("white")), "row 2 is outside");
}

#[test]
fn adjacent_rects_abut_without_overlapping_or_leaving_a_seam() {
    // The join between two boxes is where an off-by-one shows up as either a
    // double-painted column or an unpainted one.
    let canvas = rasterize(
        &list(vec![
            fill(0.0, 0.0, 5.0, 4.0, "red"),
            fill(5.0, 0.0, 5.0, 4.0, "blue"),
        ]),
        10,
        4,
        color("white"),
    )
    .expect("rasterizes");

    assert_eq!(canvas.pixel(4, 0), Some(color("red")), "last red column");
    assert_eq!(canvas.pixel(5, 0), Some(color("blue")), "first blue column");
    assert!(
        canvas.pixels().iter().all(|&p| p != color("white")),
        "no seam of unpainted background between them"
    );
}

#[test]
fn a_zero_sized_rect_paints_nothing() {
    let canvas = rasterize(
        &list(vec![
            fill(1.0, 1.0, 0.0, 5.0, "red"),
            fill(1.0, 1.0, 5.0, 0.0, "blue"),
        ]),
        4,
        4,
        color("white"),
    )
    .expect("rasterizes");
    assert!(canvas.pixels().iter().all(|&p| p == color("white")));
}

#[test]
fn fractional_coordinates_round_consistently_at_both_edges() {
    // Truncating instead of rounding pulls every edge toward zero, so a box
    // starting at 10.6 and a box ending at 10.6 would both land on column 10
    // and overlap. Rounding both edges the same way keeps them abutting.
    let canvas = rasterize(
        &list(vec![
            fill(0.0, 0.0, 10.6, 4.0, "red"),
            fill(10.6, 0.0, 5.0, 4.0, "blue"),
        ]),
        20,
        4,
        color("white"),
    )
    .expect("rasterizes");

    assert_eq!(canvas.pixel(10, 0), Some(color("red")), "10.6 rounds to 11");
    assert_eq!(canvas.pixel(11, 0), Some(color("blue")));
}

// -- clipping ------------------------------------------------------------

#[test]
fn a_rect_extending_past_the_canvas_is_clipped_not_wrapped() {
    // Without clamping, a row that runs past the right edge continues into the
    // start of the next row, which draws a diagonal smear that looks like a
    // rendering bug in something else entirely.
    let canvas = rasterize(
        &list(vec![fill(2.0, 0.0, 100.0, 1.0, "red")]),
        4,
        3,
        color("white"),
    )
    .expect("rasterizes");

    assert_eq!(canvas.pixel(3, 0), Some(color("red")));
    assert_eq!(
        canvas.pixel(0, 1),
        Some(color("white")),
        "the overflow must not wrap onto the next row"
    );
}

#[test]
fn negative_coordinates_are_clipped_not_panicked_on() {
    // Spans -10 to 2, so it clips at the origin and covers columns 0 and 1
    // only. Choosing a rect that happened to cover the whole canvas would pass
    // whether or not the negative side was clamped.
    let canvas = rasterize(
        &list(vec![fill(-10.0, -10.0, 12.0, 12.0, "red")]),
        4,
        4,
        color("white"),
    )
    .expect("rasterizes");

    assert_eq!(canvas.pixel(0, 0), Some(color("red")));
    assert_eq!(canvas.pixel(1, 1), Some(color("red")));
    assert_eq!(canvas.pixel(2, 2), Some(color("white")), "clipped at 2");
    assert_eq!(canvas.pixel(3, 3), Some(color("white")));
}

#[test]
fn a_rect_entirely_offscreen_paints_nothing() {
    let canvas = rasterize(
        &list(vec![
            fill(100.0, 100.0, 10.0, 10.0, "red"),
            fill(-50.0, -50.0, 10.0, 10.0, "blue"),
        ]),
        4,
        4,
        color("white"),
    )
    .expect("rasterizes");
    assert!(canvas.pixels().iter().all(|&p| p == color("white")));
}

// -- paint order ---------------------------------------------------------

#[test]
fn later_items_overwrite_earlier_ones() {
    // The display list's ordering is only meaningful if this holds. Drawing in
    // reverse, or skipping already-covered pixels, yields an image that looks
    // reasonable and puts the wrong thing on top wherever content overlaps.
    let canvas = rasterize(
        &list(vec![
            fill(0.0, 0.0, 4.0, 4.0, "red"),
            fill(0.0, 0.0, 4.0, 4.0, "blue"),
        ]),
        4,
        4,
        color("white"),
    )
    .expect("rasterizes");

    assert!(canvas.pixels().iter().all(|&p| p == color("blue")));
}

#[test]
fn partial_overlap_keeps_both_visible_regions() {
    let canvas = rasterize(
        &list(vec![
            fill(0.0, 0.0, 4.0, 4.0, "red"),
            fill(2.0, 0.0, 4.0, 4.0, "blue"),
        ]),
        6,
        4,
        color("white"),
    )
    .expect("rasterizes");

    assert_eq!(canvas.pixel(0, 0), Some(color("red")), "left stays red");
    assert_eq!(canvas.pixel(2, 0), Some(color("blue")), "overlap goes blue");
    assert_eq!(canvas.pixel(5, 0), Some(color("blue")));
}

// -- refusals ------------------------------------------------------------

#[test]
fn text_is_refused_rather_than_drawn_as_shapes() {
    // WP-009 carries an unresolved text-font-foundation-review gate. Drawing
    // blocks where glyphs belong would produce something that looks like a
    // rendered page, invites comparison against a real renderer, and is not
    // text.
    let result = rasterize(
        &list(vec![DisplayItem::Text {
            rect: rect(0.0, 0.0, 10.0, 10.0),
            text: "hello".to_string(),
            color: color("black"),
        }]),
        16,
        16,
        color("white"),
    );
    assert!(matches!(
        result,
        Err(RasterError::GlyphRasterizationUnsupported { ref text }) if text == "hello"
    ));
}

#[test]
fn an_oversized_canvas_is_refused_rather_than_allocated() {
    // Canvas dimensions trace back to a viewport, so an unbounded allocation
    // driven by document-influenced input is a denial of service.
    let result = Canvas::new(MAX_PIXELS, 2, color("white"));
    assert!(matches!(result, Err(RasterError::CanvasTooLarge { .. })));
}

#[test]
fn a_canvas_size_that_would_overflow_is_refused() {
    // On a 32-bit host the product of two plausible dimensions can wrap to a
    // small number, and the allocation would then succeed at the wrong size.
    let result = Canvas::new(usize::MAX, 4, color("white"));
    assert!(matches!(result, Err(RasterError::CanvasTooLarge { .. })));
}

#[test]
fn an_unparseable_colour_is_refused_by_the_value_layer() {
    // The rasterizer never sees an invalid colour because parsing happens once,
    // in turing-css. Defaulting to black at paint time would render a plausible
    // wrong colour that nobody notices.
    assert!(Color::parse("rgb(1, 2, 3)").is_err());
    assert!(Color::parse("#12345").is_err());
    assert!(Color::parse("rebeccapurple").is_err());
}

// -- canvas basics -------------------------------------------------------

#[test]
fn an_empty_display_list_yields_the_background() {
    let canvas = rasterize(&list(Vec::new()), 3, 2, color("silver")).expect("rasterizes");
    assert_eq!(canvas.width(), 3);
    assert_eq!(canvas.height(), 2);
    assert_eq!(canvas.pixels().len(), 6);
    assert!(canvas.pixels().iter().all(|&p| p == color("silver")));
}

#[test]
fn a_pixel_outside_the_canvas_is_none_rather_than_wrapping() {
    let canvas = rasterize(&list(Vec::new()), 3, 2, color("white")).expect("rasterizes");
    assert_eq!(canvas.pixel(3, 0), None);
    assert_eq!(canvas.pixel(0, 2), None);
    assert!(canvas.pixel(2, 1).is_some());
}

#[test]
fn a_zero_dimension_canvas_is_valid_and_empty() {
    let canvas = rasterize(
        &list(vec![fill(0.0, 0.0, 5.0, 5.0, "red")]),
        0,
        5,
        color("white"),
    )
    .expect("rasterizes");
    assert!(canvas.pixels().is_empty());
}
