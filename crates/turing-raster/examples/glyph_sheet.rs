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
use std::process::ExitCode;

use turing_css::Color;
use turing_layout::{DisplayItem, DisplayList, Rect};
use turing_raster::{Canvas, encode_bmp, rasterize};

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
            alpha: 1.0,
        });
    }
    list
}

fn write_bmp(canvas: &Canvas, path: &str) -> std::io::Result<()> {
    std::fs::write(path, encode_bmp(canvas))
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
