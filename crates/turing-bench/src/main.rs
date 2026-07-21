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
        "{:<12} {:>10} {:>10} {:>10} {:>18} {:>7}",
        "stage", "min", "median", "max", "median 95% CI", "CoV"
    );

    for result in run() {
        // Formatted to owned strings first: a width applies to the whole
        // argument, and `format_args!` would be padded as one unit rather than
        // producing an aligned column.
        let measurement = result.measurement;
        let ci = format!(
            "{:?}-{:?}",
            measurement.median_ci_low, measurement.median_ci_high
        );
        #[allow(clippy::cast_precision_loss)]
        let cov = format!("{:.1}%", measurement.cov_permille as f64 / 10.0);
        println!(
            "{:<12} {:>10} {:>10} {:>10} {:>18} {:>7}",
            result.stage,
            format!("{:?}", measurement.min),
            format!("{:?}", measurement.median),
            format!("{:?}", measurement.max),
            ci,
            cov,
        );
    }

    println!();
    println!(
        "median 95% CI: distribution-free interval from the order statistics; \n\
         two runs whose intervals do not overlap differ beyond this run's noise."
    );
    println!(
        "CoV: coefficient of variation (std dev / mean); a high value means the \n\
         stage is measuring the machine as much as the code."
    );
    println!("External dependencies: 0");
    println!("These are raw baselines for tracking this engine against itself.");
    println!("No comparison against another engine is implied or supported.");
}
