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
use std::process::ExitCode;

use turing_engine::Page;
use turing_raster::{Canvas, encode_bmp};

fn write_bmp(canvas: &Canvas, path: &str) -> std::io::Result<()> {
    std::fs::write(path, encode_bmp(canvas))
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
