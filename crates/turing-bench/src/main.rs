// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Runs the pipeline benchmark and prints per-stage baselines.
//!
//! Run with `cargo run --release -p turing-bench`. A debug build measures the
//! unoptimised code and is not a baseline; the output says so rather than
//! leaving it to be misread.

#![forbid(unsafe_code)]

use turing_bench::{SAMPLES, WARMUP, run};

fn main() {
    println!("Turing pipeline baselines");
    println!("{WARMUP} warm-up iterations discarded, {SAMPLES} recorded per stage");
    if cfg!(debug_assertions) {
        println!();
        println!(
            "WARNING: debug build. These numbers measure unoptimised code and \
             are not a baseline. Re-run with --release."
        );
    }
    println!();
    println!(
        "{:<12} {:>12} {:>12} {:>12}",
        "stage", "min", "median", "max"
    );

    for result in run() {
        // Formatted to owned strings first: a width applies to the whole
        // argument, and `format_args!` would be padded as one unit rather than
        // producing an aligned column.
        println!(
            "{:<12} {:>12} {:>12} {:>12}",
            result.stage,
            format!("{:?}", result.measurement.min),
            format!("{:?}", result.measurement.median),
            format!("{:?}", result.measurement.max),
        );
    }

    println!();
    println!("External dependencies: 0");
    println!("These are raw baselines for tracking this engine against itself.");
    println!("No comparison against another engine is implied or supported.");
}
