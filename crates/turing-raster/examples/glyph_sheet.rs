// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Renders the full reference glyph set to a BMP file for visual inspection.
//!
//! Usage: `cargo run -p turing-raster --example glyph_sheet -- out.bmp`
//!
//! The sheet exists because the glyph table is transcribed data: a wrong hex
//! byte produces a legible-looking but wrong glyph that no pixel test written
//! against the same table would catch. Eyes catch it immediately.

use std::env;
use std::fs::File;
use std::io::{BufWriter, Write as _};
use std::process::ExitCode;

use turing_css::Color;
use turing_layout::{DisplayItem, DisplayList, Rect};
use turing_raster::{Canvas, rasterize};

const LINE_HEIGHT: f32 = 16.0;
const ADVANCE: f32 = 8.0;

fn sheet() -> DisplayList {
    let mut list = DisplayList::default();
    let lines = [
        " !\"#$%&'()*+,-./0123456789:;<=>?",
        "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_",
        "`abcdefghijklmnopqrstuvwxyz{|}~",
        "",
        "Sphinx of black quartz, judge my vow.",
        "pack my box with five dozen liquor jugs",
        "0123456789 +-*/= <html> {out: \"of\"} 100%",
    ];
    for (row, line) in lines.iter().enumerate() {
        #[allow(clippy::cast_precision_loss)]
        let width = line.chars().count() as f32 * ADVANCE;
        list.items.push(DisplayItem::Text {
            rect: Rect {
                x: ADVANCE,
                #[allow(clippy::cast_precision_loss)]
                y: (row as f32).mul_add(LINE_HEIGHT, LINE_HEIGHT / 2.0),
                width,
                height: LINE_HEIGHT,
            },
            text: (*line).to_owned(),
            color: Color {
                red: 0,
                green: 0,
                blue: 0,
            },
        });
    }
    list
}

/// Writes `canvas` as an uncompressed 24-bit BMP.
fn write_bmp(canvas: &Canvas, path: &str) -> std::io::Result<()> {
    let width = canvas.width();
    let height = canvas.height();
    // Each BMP pixel row is padded to a multiple of four bytes.
    let row_bytes = (width * 3).div_ceil(4) * 4;
    let pixel_bytes = row_bytes * height;
    let file_bytes = 54 + pixel_bytes;

    let mut out = BufWriter::new(File::create(path)?);
    let u32le = |value: usize| u32::try_from(value).expect("fits").to_le_bytes();

    out.write_all(b"BM")?;
    out.write_all(&u32le(file_bytes))?;
    out.write_all(&[0; 4])?; // reserved
    out.write_all(&u32le(54))?; // pixel data offset
    out.write_all(&u32le(40))?; // BITMAPINFOHEADER size
    out.write_all(&u32le(width))?;
    out.write_all(&u32le(height))?;
    out.write_all(&1u16.to_le_bytes())?; // planes
    out.write_all(&24u16.to_le_bytes())?; // bits per pixel
    out.write_all(&[0; 24])?; // no compression, defaulted remainder

    // BMP stores rows bottom-up.
    for y in (0..height).rev() {
        let mut row = Vec::with_capacity(row_bytes);
        for x in 0..width {
            let pixel = canvas.pixel(x, y).expect("in bounds");
            row.extend_from_slice(&[pixel.blue, pixel.green, pixel.red]);
        }
        row.resize(row_bytes, 0);
        out.write_all(&row)?;
    }
    out.flush()
}

fn main() -> ExitCode {
    let Some(path) = env::args().nth(1) else {
        eprintln!("usage: glyph_sheet <output.bmp>");
        return ExitCode::FAILURE;
    };
    let background = Color {
        red: 255,
        green: 255,
        blue: 255,
    };
    let canvas = match rasterize(&sheet(), 344, 128, background) {
        Ok(canvas) => canvas,
        Err(error) => {
            eprintln!("glyph_sheet: {error}");
            return ExitCode::FAILURE;
        }
    };
    match write_bmp(&canvas, &path) {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("glyph_sheet: {error}");
            ExitCode::FAILURE
        }
    }
}
