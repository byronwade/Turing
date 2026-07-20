// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! One-shot cold pipeline timing: load and paint a page exactly once, in a
//! fresh process, and print the microsecond costs.
//!
//! Usage: `cargo run --release -p turing-engine --example cold_load -- page.html [width] [height]`
//!
//! This exists for cross-engine comparison, where the other engine's number
//! is a cold navigation: a warm-loop median (what `turing-bench` reports)
//! measures a hot cache and amortised allocation, which is a different
//! quantity. Run this several times — one process per run — and take the
//! median of the printed numbers.

use std::env;
use std::process::ExitCode;
use std::time::Instant;

use turing_engine::Page;

fn run() -> Result<(), String> {
    let mut args = env::args().skip(1);
    let Some(input) = args.next() else {
        return Err("usage: cold_load <page.html> [width] [height]".to_owned());
    };
    let width: usize = args
        .next()
        .map_or(Ok(1280), |raw| raw.parse())
        .map_err(|error| format!("width: {error}"))?;
    let height: usize = args
        .next()
        .map_or(Ok(720), |raw| raw.parse())
        .map_err(|error| format!("height: {error}"))?;
    let html =
        std::fs::read_to_string(&input).map_err(|error| format!("cannot read {input}: {error}"))?;

    // Load covers tokenize, tree build, style parse, script, cascade, and
    // layout — the same span Chrome's ParseHTML + style + layout events
    // cover for a page with inline styles and no subresources.
    let started = Instant::now();
    #[allow(clippy::cast_precision_loss)]
    let page = Page::load(&html, width as f32).map_err(|error| error.to_string())?;
    let load = started.elapsed();

    let started = Instant::now();
    let list = page.display_list();
    let display_list = started.elapsed();

    let started = Instant::now();
    let canvas = turing_raster::rasterize(
        &list,
        width,
        height,
        turing_css::Color {
            red: 255,
            green: 255,
            blue: 255,
        },
    )
    .map_err(|error| error.to_string())?;
    let raster = started.elapsed();

    // The canvas participates in output so the work cannot be optimised out.
    println!(
        "load_us={} display_list_us={} raster_us={} pixels={}",
        load.as_micros(),
        display_list.as_micros(),
        raster.as_micros(),
        canvas.pixels().len()
    );
    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("cold_load: {error}");
            ExitCode::FAILURE
        }
    }
}
