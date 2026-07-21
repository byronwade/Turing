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
//! # How text is drawn
//!
//! `DisplayItem::Text` paints with the embedded 8x8 public-domain bitmap font
//! in [`mod@font`], per the owner decision recorded in
//! `docs/research/text-font-foundation-decision-2026-07.md`. A text item is a
//! single line run — layout breaks lines between inline children, never inside
//! one — so painting is a per-character blit: the advance is recovered from the
//! run's rect (layout sized it as `chars x advance`), and each glyph is centred
//! vertically in the run's line box. Characters outside printable ASCII draw a
//! hollow replacement box rather than nothing, so missing coverage stays
//! visible.
//!
//! This glyph set is the reference painter's text foundation only. Shaping,
//! hinting, subpixel positioning, Unicode coverage, and the product font stack
//! remain undecided, and [`turing_layout::TextMetrics`] remains an injected
//! measurement — the default 8-per-advance metric and this font agree by
//! construction, and a caller who injects different metrics gets glyphs spaced
//! to their metrics, not resized.
//!
//! # Deliberate limits
//!
//! Colours are opaque. Alpha requires compositing rules — what a translucent
//! colour blends against depends on stacking order and group opacity — so
//! compositing here is a plain overwrite in paint order. That is exact for
//! opaque fills and is refused rather than approximated for anything else, at
//! the point where [`turing_css::Color`] declines to parse it.

#![forbid(unsafe_code)]

mod font;

/// The reference glyph bitmap for `character`: eight rows, bit 0 leftmost.
///
/// Public so a second painter draws the same glyphs the reference draws;
/// two painters with two fonts cannot be diffed.
#[must_use]
pub fn glyph_rows(character: char) -> &'static [u8; 8] {
    font::glyph(character)
}

use core::fmt;
use turing_css::Color;
use turing_layout::{DisplayItem, DisplayList, Rect};

/// A construct this rasterizer does not draw.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum RasterError {
    /// The requested canvas is larger than this rasterizer will allocate.
    CanvasTooLarge { width: usize, height: usize },
}

impl fmt::Display for RasterError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
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

    /// Wraps an existing pixel buffer as a canvas.
    ///
    /// Exists so a second painter can produce the same artifact type this
    /// reference produces and be diffed against it pixel for pixel.
    ///
    /// # Errors
    ///
    /// Returns [`RasterError::CanvasTooLarge`] when `pixels` is not exactly
    /// `width x height` or exceeds [`MAX_PIXELS`].
    pub fn from_pixels(
        width: usize,
        height: usize,
        pixels: Vec<Color>,
    ) -> Result<Self, RasterError> {
        let expected = width
            .checked_mul(height)
            .filter(|&count| count <= MAX_PIXELS && count == pixels.len())
            .ok_or(RasterError::CanvasTooLarge { width, height })?;
        debug_assert_eq!(expected, pixels.len());
        Ok(Self {
            width,
            height,
            pixels,
        })
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

    /// Draws a single-line text run into `rect` with `color`.
    ///
    /// Layout sized the run's rect as `character count x advance`, so the
    /// advance is recovered by dividing rather than assumed, and glyphs follow
    /// whatever metric the caller injected into layout. The 8x8 glyph is
    /// centred vertically in the run's line box and clipped to the canvas like
    /// every other draw.
    fn draw_text(&mut self, rect: Rect, text: &str, color: Color) {
        let count = text.chars().count();
        if count == 0 {
            return;
        }
        #[allow(clippy::cast_precision_loss)]
        let advance = rect.width / count as f32;
        let glyph_size = font::GLYPH_SIZE as f32;
        let top = round_to_pixel(rect.y + (rect.height - glyph_size) / 2.0);

        for (index, character) in text.chars().enumerate() {
            #[allow(clippy::cast_precision_loss)]
            let left = round_to_pixel(rect.x + index as f32 * advance);
            self.blit_glyph(font::glyph(character), left, top, color);
        }
    }

    /// Blits one glyph bitmap with its top-left corner at `(left, top)`.
    fn blit_glyph(&mut self, rows: &[u8; 8], left: i64, top: i64, color: Color) {
        for (row, bits) in rows.iter().enumerate() {
            let y = top + as_i64(row);
            if y < 0 || y >= as_i64(self.height) {
                continue;
            }
            for column in 0..font::GLYPH_SIZE {
                // Bit 0 is the leftmost column; see the encoding note in `font`.
                if bits & (1 << column) == 0 {
                    continue;
                }
                let x = left + as_i64(column);
                if x < 0 || x >= as_i64(self.width) {
                    continue;
                }
                let index = (y as usize) * self.width + (x as usize);
                self.pixels[index] = color;
            }
        }
    }
}

/// Encodes `canvas` as an uncompressed 24-bit BMP file.
///
/// BMP because it is the simplest self-contained image container that
/// standard viewers open: a fixed 54-byte header and bottom-up rows padded to
/// four bytes, writable without a dependency. This is how lab renders become
/// inspectable artifacts.
#[must_use]
pub fn encode_bmp(canvas: &Canvas) -> Vec<u8> {
    let width = canvas.width();
    let height = canvas.height();
    let row_bytes = (width * 3).div_ceil(4) * 4;
    let file_bytes = 54 + row_bytes * height;

    let mut out = Vec::with_capacity(file_bytes);
    let u32le = |value: usize| u32::try_from(value).unwrap_or(u32::MAX).to_le_bytes();
    out.extend_from_slice(b"BM");
    out.extend_from_slice(&u32le(file_bytes));
    out.extend_from_slice(&[0; 4]); // reserved
    out.extend_from_slice(&u32le(54)); // pixel data offset
    out.extend_from_slice(&u32le(40)); // BITMAPINFOHEADER size
    out.extend_from_slice(&u32le(width));
    out.extend_from_slice(&u32le(height));
    out.extend_from_slice(&1u16.to_le_bytes()); // planes
    out.extend_from_slice(&24u16.to_le_bytes()); // bits per pixel
    out.extend_from_slice(&[0; 24]); // no compression, defaulted remainder

    // Rows are stored bottom-up.
    for y in (0..height).rev() {
        let row_start = out.len();
        for x in 0..width {
            let pixel = canvas.pixel(x, y).unwrap_or(Color {
                red: 0,
                green: 0,
                blue: 0,
            });
            out.extend_from_slice(&[pixel.blue, pixel.green, pixel.red]);
        }
        out.resize(row_start + row_bytes, 0);
    }
    out
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
/// Returns [`RasterError`] for a canvas beyond [`MAX_PIXELS`].
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
            // The reference does not round: it fills the rectangle squarely,
            // which is the honest "this painter cannot express a radius"
            // behaviour a compositing painter is diffed against.
            DisplayItem::RoundedColor { rect, color, .. } => canvas.fill(*rect, *color),
            DisplayItem::Text { rect, text, color } => canvas.draw_text(*rect, text, *color),
        }
    }
    Ok(canvas)
}
