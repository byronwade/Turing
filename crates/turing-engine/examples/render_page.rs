// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Headless page render: HTML file in, BMP file out.
//!
//! Usage: `cargo run -p turing-engine --example render_page -- page.html out.bmp [width] [height]`
//!
//! This is the windowed presenter minus the window — the same `Page`, the
//! same pixels — which makes it the reproducible artifact for "what does the
//! engine draw for this file", with no display required.

use std::env;
use std::fs::File;
use std::io::{BufWriter, Write as _};
use std::process::ExitCode;

use turing_engine::Page;
use turing_raster::Canvas;

fn write_bmp(canvas: &Canvas, path: &str) -> std::io::Result<()> {
    let width = canvas.width();
    let height = canvas.height();
    let row_bytes = (width * 3).div_ceil(4) * 4;
    let file_bytes = 54 + row_bytes * height;

    let mut out = BufWriter::new(File::create(path)?);
    let u32le = |value: usize| u32::try_from(value).expect("fits").to_le_bytes();
    out.write_all(b"BM")?;
    out.write_all(&u32le(file_bytes))?;
    out.write_all(&[0; 4])?;
    out.write_all(&u32le(54))?;
    out.write_all(&u32le(40))?;
    out.write_all(&u32le(width))?;
    out.write_all(&u32le(height))?;
    out.write_all(&1u16.to_le_bytes())?;
    out.write_all(&24u16.to_le_bytes())?;
    out.write_all(&[0; 24])?;
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

fn run() -> Result<(), String> {
    let mut args = env::args().skip(1);
    let (Some(input), Some(output)) = (args.next(), args.next()) else {
        return Err("usage: render_page <page.html> <out.bmp> [width] [height]".to_owned());
    };
    let width: usize = args
        .next()
        .map_or(Ok(800), |raw| raw.parse())
        .map_err(|error| format!("width: {error}"))?;
    let height: usize = args
        .next()
        .map_or(Ok(600), |raw| raw.parse())
        .map_err(|error| format!("height: {error}"))?;

    let html =
        std::fs::read_to_string(&input).map_err(|error| format!("cannot read {input}: {error}"))?;
    #[allow(clippy::cast_precision_loss)]
    let page = Page::load(&html, width as f32).map_err(|error| error.to_string())?;
    let canvas = page
        .render(width, height)
        .map_err(|error| error.to_string())?;
    write_bmp(&canvas, &output).map_err(|error| format!("cannot write {output}: {error}"))?;
    if let Some(title) = page.title() {
        println!("rendered {title:?} to {output} ({width}x{height})");
    } else {
        println!("rendered {input} to {output} ({width}x{height})");
    }
    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("render_page: {error}");
            ExitCode::FAILURE
        }
    }
}
