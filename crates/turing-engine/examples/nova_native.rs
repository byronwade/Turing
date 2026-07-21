// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Milestone 1 of the native React-runtime plan (owner decision,
//! 2026-07-21 — see the `turing-nova-source-real-scope` project memory
//! for the full history and the `docs/ui-runtime/design-lab/README.md`
//! amendment): compile, and eventually render, the literal, never-edited
//! `docs/ui-runtime/design-lab/turing-nova-design-source.jsx` — not a
//! hand-extracted fragment, the actual 7,727-line file — through
//! `turing-js`'s own `import`/`export` support and the shared prelude's
//! first-render-only hook shims.
//!
//! `include_str!` embeds the file at compile time from its real,
//! CI-validated location; nothing here copies or edits it.
//!
//! Run with `cargo run -p turing-engine --example nova_native` — reports
//! the first compile error (this milestone is not render-ready yet) so
//! the empirical loop this file exists for has one command to run.

use turing_js::{JsError, compile};

#[path = "common/mod.rs"]
mod common;
use common::PRELUDE;

const NOVA_SOURCE: &str =
    include_str!("../../../docs/ui-runtime/design-lab/turing-nova-design-source.jsx");

fn main() {
    let program = format!("{PRELUDE}{NOVA_SOURCE}");
    match compile(&program) {
        Ok(_) => {
            println!("compile OK — the literal Nova file compiles end to end.");
        }
        Err(error) => {
            println!("compile FAIL: {error}");
            // `error`'s own byte offset, where it has one, is into the
            // *combined* prelude+source string compile() actually saw —
            // report the offset within the real file alone too, since
            // that is what a source-line lookup in an editor needs.
            if let JsError::UnexpectedCharacter { offset, .. } = error
                && offset >= PRELUDE.len()
            {
                let nova_offset = offset - PRELUDE.len();
                let line = NOVA_SOURCE[..nova_offset].matches('\n').count() + 1;
                println!("  (byte {nova_offset} of the real file, around line {line})");
            }
            std::process::exit(1);
        }
    }
}
