// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! CPU compositing painter: alpha, rounded corners, anti-aliasing.
//!
//! `turing-raster` is the reference: opaque, hard-edged, written to be read,
//! and the definition of right where the two overlap. This crate is the
//! second painter that reference exists to check — it adds the three things
//! the Nova design needs that the reference deliberately refuses: source-over
//! alpha compositing, rounded-corner fills, and anti-aliased edges.
//!
//! # The parity contract
//!
//! For any input expressible in the reference's vocabulary — every item
//! opaque and square — this painter must produce the reference's output
//! pixel for pixel. That is enforced by construction (the opaque square path
//! runs the same coverage rules: half-open intervals, rounded edges, clamped
//! bounds, later-over-earlier) and by tests that diff the two canvases
//! exactly. Alpha and radius are extensions beyond the reference's domain,
//! not deviations inside it.
//!
//! # Anti-aliasing model
//!
//! A rounded fill's coverage comes from the signed distance to the rounded
//! rectangle evaluated at the pixel centre, mapped through a one-pixel
//! linear filter (`0.5 - distance`, clamped to `[0, 1]`). That is a box
//! filter approximation: cheap, deterministic, and accurate to well under a
//! pixel, which is the right trade for a CPU painter whose correctness
//! anchor is the reference, not a typography rasteriser.

#![forbid(unsafe_code)]

use turing_css::Color;
use turing_layout::{DisplayItem, DisplayList, Rect};
use turing_raster::{Canvas, MAX_PIXELS, RasterError, glyph_rows};

/// One compositing paint command.
#[derive(Clone, Debug, PartialEq)]
pub enum PaintItem {
    /// Fill a rectangle, optionally translucent and optionally rounded.
    Fill {
        rect: Rect,
        color: Color,
        /// Opacity in `[0, 1]`; values outside are clamped.
        alpha: f32,
        /// Corner radius in CSS pixels; clamped to half the short side.
        radius: f32,
    },
    /// A single-line text run, optionally translucent.
    Text {
        rect: Rect,
        text: String,
        color: Color,
        alpha: f32,
    },
}

/// The flat, ordered list of compositing commands for one frame.
#[derive(Clone, Debug, Default, PartialEq)]
pub struct PaintList {
    /// Commands in paint order; later items composite over earlier ones.
    pub items: Vec<PaintItem>,
}

impl PaintList {
    /// Lifts an engine display list into the compositing vocabulary:
    /// everything square except a resolved `border-radius`, everything
    /// opaque except a resolved `opacity` — the two respects in which this
    /// painter is a real compositor rather than the reference it is diffed
    /// against.
    #[must_use]
    pub fn from_display_list(list: &DisplayList) -> Self {
        let items = list
            .items
            .iter()
            .map(|item| match item {
                DisplayItem::SolidColor { rect, color, alpha } => PaintItem::Fill {
                    rect: *rect,
                    color: *color,
                    alpha: *alpha,
                    radius: 0.0,
                },
                DisplayItem::RoundedColor {
                    rect,
                    color,
                    radius,
                    alpha,
                } => PaintItem::Fill {
                    rect: *rect,
                    color: *color,
                    alpha: *alpha,
                    radius: *radius,
                },
                DisplayItem::Text {
                    rect,
                    text,
                    color,
                    alpha,
                } => PaintItem::Text {
                    rect: *rect,
                    text: text.clone(),
                    color: *color,
                    alpha: *alpha,
                },
            })
            .collect();
        Self { items }
    }
}

/// Paints `list` onto a `width` by `height` canvas over `background`.
///
/// # Errors
///
/// Returns [`RasterError::CanvasTooLarge`] beyond [`MAX_PIXELS`], the same
/// bound the reference enforces — a second painter must not be the one that
/// forgets the allocation limit.
pub fn paint(
    list: &PaintList,
    width: usize,
    height: usize,
    background: Color,
) -> Result<Canvas, RasterError> {
    let count = width
        .checked_mul(height)
        .filter(|&count| count <= MAX_PIXELS)
        .ok_or(RasterError::CanvasTooLarge { width, height })?;
    let mut pixels = vec![background; count];

    for item in &list.items {
        match item {
            PaintItem::Fill {
                rect,
                color,
                alpha,
                radius,
            } => fill(&mut pixels, width, height, *rect, *color, *alpha, *radius),
            PaintItem::Text {
                rect,
                text,
                color,
                alpha,
            } => draw_text(&mut pixels, width, height, *rect, text, *color, *alpha),
        }
    }
    Canvas::from_pixels(width, height, pixels)
}

/// Source-over blend of `src` at `alpha` onto one channel.
fn blend_channel(src: u8, dst: u8, alpha: f32) -> u8 {
    let value = f32::from(src).mul_add(alpha, f32::from(dst) * (1.0 - alpha));
    #[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
    {
        value.round().clamp(0.0, 255.0) as u8
    }
}

fn blend(pixels: &mut [Color], index: usize, color: Color, alpha: f32) {
    if alpha >= 1.0 {
        pixels[index] = color;
        return;
    }
    if alpha <= 0.0 {
        return;
    }
    let dst = pixels[index];
    pixels[index] = Color {
        red: blend_channel(color.red, dst.red, alpha),
        green: blend_channel(color.green, dst.green, alpha),
        blue: blend_channel(color.blue, dst.blue, alpha),
    };
}

fn round_to_pixel(value: f32) -> i64 {
    // Identical to the reference: away-from-zero at .5, consistent for both
    // edges, which is what keeps adjacent boxes from overlapping or seaming.
    value.round() as i64
}

fn as_i64(value: usize) -> i64 {
    i64::try_from(value).unwrap_or(i64::MAX)
}

/// Fills `rect`, dispatching between the reference-exact square path and the
/// anti-aliased rounded path.
fn fill(
    pixels: &mut [Color],
    width: usize,
    height: usize,
    rect: Rect,
    color: Color,
    alpha: f32,
    radius: f32,
) {
    let alpha = alpha.clamp(0.0, 1.0);
    if alpha <= 0.0 || rect.width <= 0.0 || rect.height <= 0.0 {
        return;
    }
    let radius = radius.clamp(0.0, rect.width.min(rect.height) / 2.0);

    if radius == 0.0 {
        // The reference's coverage rules, verbatim: half-open interval,
        // rounded edges, clamped to the canvas. With alpha 1 this overwrites
        // exactly the pixels the reference overwrites, which is the parity
        // contract.
        let left = round_to_pixel(rect.x).max(0);
        let top = round_to_pixel(rect.y).max(0);
        let right = round_to_pixel(rect.x + rect.width).min(as_i64(width));
        let bottom = round_to_pixel(rect.y + rect.height).min(as_i64(height));
        for y in top..bottom {
            for x in left..right {
                let index = (y as usize) * width + (x as usize);
                blend(pixels, index, color, alpha);
            }
        }
        return;
    }

    // Rounded path: signed distance at pixel centres over the rect's
    // bounds, expanded one pixel so the anti-aliased fringe is not clipped.
    let left = round_to_pixel(rect.x - 1.0).max(0);
    let top = round_to_pixel(rect.y - 1.0).max(0);
    let right = round_to_pixel(rect.x + rect.width + 1.0).min(as_i64(width));
    let bottom = round_to_pixel(rect.y + rect.height + 1.0).min(as_i64(height));

    let center_x = rect.x + rect.width / 2.0;
    let center_y = rect.y + rect.height / 2.0;
    let half_x = rect.width / 2.0;
    let half_y = rect.height / 2.0;

    for y in top..bottom {
        #[allow(clippy::cast_precision_loss)]
        let py = (y as f32 + 0.5) - center_y;
        for x in left..right {
            #[allow(clippy::cast_precision_loss)]
            let px = (x as f32 + 0.5) - center_x;
            let qx = px.abs() - (half_x - radius);
            let qy = py.abs() - (half_y - radius);
            let outside = (qx.max(0.0).powi(2) + qy.max(0.0).powi(2)).sqrt();
            let inside = qx.max(qy).min(0.0);
            let distance = outside + inside - radius;
            let coverage = (0.5 - distance).clamp(0.0, 1.0);
            if coverage > 0.0 {
                let index = (y as usize) * width + (x as usize);
                blend(pixels, index, color, alpha * coverage);
            }
        }
    }
}

const GLYPH_SIZE: f32 = 8.0;
const GLYPH_CELL: usize = 8;

/// Draws a single-line run with the reference glyph set and rules: advance
/// recovered from the rect, glyphs centred in the line box, clipped to the
/// canvas. With alpha 1 this matches the reference blit exactly.
fn draw_text(
    pixels: &mut [Color],
    width: usize,
    height: usize,
    rect: Rect,
    text: &str,
    color: Color,
    alpha: f32,
) {
    let alpha = alpha.clamp(0.0, 1.0);
    let count = text.chars().count();
    if count == 0 || alpha <= 0.0 {
        return;
    }
    #[allow(clippy::cast_precision_loss)]
    let advance = rect.width / count as f32;
    let top = round_to_pixel(rect.y + (rect.height - GLYPH_SIZE) / 2.0);

    for (index, character) in text.chars().enumerate() {
        #[allow(clippy::cast_precision_loss)]
        let left = round_to_pixel(rect.x + index as f32 * advance);
        let rows = glyph_rows(character);
        for (row, bits) in rows.iter().enumerate() {
            let y = top + as_i64(row);
            if y < 0 || y >= as_i64(height) {
                continue;
            }
            for column in 0..GLYPH_CELL {
                if bits & (1u8 << column) == 0 {
                    continue;
                }
                let x = left + as_i64(column);
                if x < 0 || x >= as_i64(width) {
                    continue;
                }
                let index = (y as usize) * width + (x as usize);
                blend(pixels, index, color, alpha);
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use turing_raster::rasterize;

    fn color(name: &str) -> Color {
        Color::parse(name).expect("parses")
    }

    fn rect(x: f32, y: f32, width: f32, height: f32) -> Rect {
        Rect {
            x,
            y,
            width,
            height,
        }
    }

    #[test]
    fn opaque_square_output_is_pixel_identical_to_the_reference() {
        // Fills that clip, abut, overlap, and a text run — the reference's
        // whole vocabulary, including its edge rules.
        let display = DisplayList {
            items: vec![
                DisplayItem::SolidColor {
                    rect: rect(-3.0, -3.0, 10.0, 10.0),
                    color: color("red"),
                    alpha: 1.0,
                },
                DisplayItem::SolidColor {
                    rect: rect(4.6, 2.0, 7.9, 5.5),
                    color: color("navy"),
                    alpha: 1.0,
                },
                DisplayItem::Text {
                    rect: rect(1.0, 6.0, 24.0, 16.0),
                    text: "abc".to_owned(),
                    color: color("black"),
                    alpha: 1.0,
                },
            ],
        };
        let reference = rasterize(&display, 24, 24, color("white")).expect("rasterizes");
        let lifted = PaintList::from_display_list(&display);
        let painted = paint(&lifted, 24, 24, color("white")).expect("paints");
        assert_eq!(painted, reference, "parity with the reference broke");
    }

    #[test]
    fn a_rounded_display_item_lifts_into_a_rounded_fill() {
        let display = DisplayList {
            items: vec![DisplayItem::RoundedColor {
                rect: rect(0.0, 0.0, 20.0, 20.0),
                color: color("black"),
                radius: 8.0,
                alpha: 1.0,
            }],
        };
        let lifted = PaintList::from_display_list(&display);
        assert_eq!(
            lifted.items,
            vec![PaintItem::Fill {
                rect: rect(0.0, 0.0, 20.0, 20.0),
                color: color("black"),
                alpha: 1.0,
                radius: 8.0,
            }]
        );
        // And it actually rounds: the corner clears.
        let canvas = paint(&lifted, 20, 20, color("white")).expect("paints");
        assert_eq!(canvas.pixel(0, 0), Some(color("white")), "corner cleared");
    }

    #[test]
    fn alpha_blends_source_over() {
        let list = PaintList {
            items: vec![PaintItem::Fill {
                rect: rect(0.0, 0.0, 2.0, 2.0),
                color: color("red"),
                alpha: 0.5,
                radius: 0.0,
            }],
        };
        let canvas = paint(&list, 2, 2, color("white")).expect("paints");
        let pixel = canvas.pixel(0, 0).expect("in bounds");
        assert_eq!(pixel.red, 255, "red channel saturated on both sides");
        assert!(
            (127..=128).contains(&pixel.green),
            "half red over white halves green: {pixel:?}"
        );
    }

    #[test]
    fn rounded_corners_clear_the_corner_and_keep_the_center() {
        let list = PaintList {
            items: vec![PaintItem::Fill {
                rect: rect(0.0, 0.0, 20.0, 20.0),
                color: color("black"),
                alpha: 1.0,
                radius: 8.0,
            }],
        };
        let canvas = paint(&list, 20, 20, color("white")).expect("paints");
        assert_eq!(
            canvas.pixel(0, 0),
            Some(color("white")),
            "the corner pixel is outside an 8px radius"
        );
        assert_eq!(
            canvas.pixel(10, 10),
            Some(color("black")),
            "the centre is solid"
        );
        // On the corner arc the coverage is partial: neither background nor
        // fill, which is what anti-aliasing means.
        let arc = canvas.pixel(2, 2).expect("in bounds");
        assert!(
            arc != color("white") && arc != color("black"),
            "the arc pixel blends: {arc:?}"
        );
    }

    #[test]
    fn radius_is_clamped_to_the_short_side() {
        // A radius far beyond the geometry must degrade to a capsule, not
        // panic or invert the shape.
        let list = PaintList {
            items: vec![PaintItem::Fill {
                rect: rect(0.0, 0.0, 16.0, 8.0),
                color: color("black"),
                alpha: 1.0,
                radius: 100.0,
            }],
        };
        let canvas = paint(&list, 16, 8, color("white")).expect("paints");
        assert_eq!(canvas.pixel(8, 4), Some(color("black")), "capsule centre");
        assert_eq!(canvas.pixel(0, 0), Some(color("white")), "capsule corner");
    }

    #[test]
    fn the_allocation_bound_holds_here_too() {
        let result = paint(&PaintList::default(), usize::MAX, 4, color("white"));
        assert!(matches!(result, Err(RasterError::CanvasTooLarge { .. })));
    }
}
