// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Turing-owned CPU reference rasterizer.
//!
//! This is the "CPU reference raster" the M2 milestone gate lists as a blocking
//! output and `IF-003` names as an interface contract. It has no requirement of
//! its own; it exists under `REQ-ENG-005` as the consumer that proves the
//! display list is a complete handoff.
//!
//! # What a reference rasterizer is for
//!
//! Not speed. It is the obviously-correct implementation that a faster or
//! GPU-backed painter is diffed against, so it is written to be read rather
//! than to be quick: no tiling, no batching, no incremental damage. When the
//! two disagree, this one is the definition of right.
//!
//! # Why text is refused
//!
//! `DisplayItem::Text` returns [`RasterError::GlyphRasterizationUnsupported`].
//! Painting text needs glyph outlines from a font, and `WP-009` carries an
//! unresolved `text-font-foundation-review` decision gate — no font foundation
//! has been chosen. Drawing blocks or boxes where glyphs belong would produce
//! output that looks like a rendered page, invites comparison against a real
//! renderer, and is not text. Refusing keeps the gap visible until the gate is
//! decided.
//!
//! Layout already handles text this way: [`turing_layout::TextMetrics`] is an
//! explicit injected measurement rather than a hidden assumption. This is the
//! same principle at the paint layer, and it lands on refusal rather than
//! injection because there is no measured quantity to inject — a glyph shape is
//! not a number a caller can supply.
//!
//! # Deliberate limits
//!
//! Colours are opaque. Alpha requires compositing rules — what a translucent
//! colour blends against depends on stacking order and group opacity — so
//! compositing here is a plain overwrite in paint order. That is exact for
//! opaque fills and is refused rather than approximated for anything else, at
//! the point where [`turing_css::Color`] declines to parse it.

#![forbid(unsafe_code)]

use core::fmt;
use turing_css::Color;
use turing_layout::{DisplayItem, DisplayList, Rect};

/// A construct this rasterizer does not draw.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum RasterError {
    /// Text was present in the display list.
    GlyphRasterizationUnsupported { text: String },
    /// The requested canvas is larger than this rasterizer will allocate.
    CanvasTooLarge { width: usize, height: usize },
}

impl fmt::Display for RasterError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::GlyphRasterizationUnsupported { text } => write!(
                formatter,
                "cannot rasterize the text {text:?}: no font foundation has been \
                 selected, and drawing shapes where glyphs belong would look like \
                 a rendered page without being one"
            ),
            Self::CanvasTooLarge { width, height } => write!(
                formatter,
                "a {width}x{height} canvas exceeds the reference rasterizer's limit; \
                 a display list should not be able to choose an allocation size"
            ),
        }
    }
}

/// The largest canvas this rasterizer will allocate, in pixels.
///
/// Present because canvas dimensions ultimately trace back to a viewport size,
/// and an unbounded allocation driven by document-influenced input is a denial
/// of service. Sixty-four megapixels is far above any real viewport.
pub const MAX_PIXELS: usize = 64 * 1024 * 1024;

/// A rectangular grid of opaque sRGB pixels, in row-major order.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Canvas {
    width: usize,
    height: usize,
    pixels: Vec<Color>,
}

impl Canvas {
    /// Creates a canvas filled with `background`.
    ///
    /// # Errors
    ///
    /// Returns [`RasterError::CanvasTooLarge`] beyond [`MAX_PIXELS`].
    pub fn new(width: usize, height: usize, background: Color) -> Result<Self, RasterError> {
        // Checked rather than wrapping: on a 32-bit host the product of two
        // plausible dimensions can overflow to a small number, and the
        // allocation would then succeed at the wrong size.
        let count = width
            .checked_mul(height)
            .filter(|&count| count <= MAX_PIXELS)
            .ok_or(RasterError::CanvasTooLarge { width, height })?;
        Ok(Self {
            width,
            height,
            pixels: vec![background; count],
        })
    }

    #[must_use]
    pub fn width(&self) -> usize {
        self.width
    }

    #[must_use]
    pub fn height(&self) -> usize {
        self.height
    }

    /// Returns the pixel at `(x, y)`, or `None` when outside the canvas.
    #[must_use]
    pub fn pixel(&self, x: usize, y: usize) -> Option<Color> {
        if x >= self.width || y >= self.height {
            return None;
        }
        self.pixels.get(y * self.width + x).copied()
    }

    /// Returns the pixels in row-major order.
    #[must_use]
    pub fn pixels(&self) -> &[Color] {
        &self.pixels
    }

    /// Fills `rect` with `color`, clipped to the canvas.
    ///
    /// Coverage is half-open: a rect at `x = 0` with `width = 10` covers columns
    /// 0 through 9. Closing the interval would make every fill one pixel wider
    /// than it should be and make adjacent boxes overlap by a pixel, which is
    /// invisible in a single-box test and wrong everywhere.
    fn fill(&mut self, rect: Rect, color: Color) {
        // Rounding, not truncation. Truncating pulls every edge toward zero, so
        // a box at x = 10.6 starts at column 10 while a box ending at 10.6 also
        // ends at 10 — the two would overlap rather than abut.
        let left = round_to_pixel(rect.x).max(0);
        let top = round_to_pixel(rect.y).max(0);
        let right = round_to_pixel(rect.x + rect.width).min(as_i64(self.width));
        let bottom = round_to_pixel(rect.y + rect.height).min(as_i64(self.height));

        // A zero-width or zero-height rect covers nothing. An empty range is
        // not an error and must not produce a single pixel.
        for y in top..bottom {
            for x in left..right {
                let index = (y as usize) * self.width + (x as usize);
                self.pixels[index] = color;
            }
        }
    }
}

fn round_to_pixel(value: f32) -> i64 {
    // `f32::round` is away-from-zero at .5; that is fine and, more importantly,
    // it is consistent for both edges of every rect, which is what keeps
    // adjacent boxes from overlapping or leaving a seam.
    value.round() as i64
}

fn as_i64(value: usize) -> i64 {
    i64::try_from(value).unwrap_or(i64::MAX)
}

/// Rasterizes `list` onto a `width` by `height` canvas over `background`.
///
/// Items are drawn in list order and later items overwrite earlier ones, which
/// is what makes the display list's ordering meaningful. Drawing in reverse, or
/// skipping already-covered pixels, produces an image that looks reasonable and
/// puts the wrong content on top wherever anything overlaps.
///
/// # Errors
///
/// Returns [`RasterError`] for text, which needs a font foundation that has not
/// been selected, and for a canvas beyond [`MAX_PIXELS`].
pub fn rasterize(
    list: &DisplayList,
    width: usize,
    height: usize,
    background: Color,
) -> Result<Canvas, RasterError> {
    let mut canvas = Canvas::new(width, height, background)?;
    for item in &list.items {
        match item {
            DisplayItem::SolidColor { rect, color } => canvas.fill(*rect, *color),
            DisplayItem::Text { text, .. } => {
                return Err(RasterError::GlyphRasterizationUnsupported { text: text.clone() });
            }
        }
    }
    Ok(canvas)
}
