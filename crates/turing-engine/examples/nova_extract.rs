// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! The extraction path `docs/ui-runtime/design-lab/README.md` documents:
//! components pulled from `docs/ui-runtime/design-lab/turing-nova-design-source.jsx`
//! (never edited, never executed — see that README and
//! `[[turing-nova-source-real-scope]]` in memory for why), rewritten as
//! turing-js-dialect code (no `react`/`lucide-react` imports; ordinary
//! top-level components) and grown against the *real* compiler one
//! component at a time. Each component below is annotated with the line
//! range it was extracted from, so a diff against the original stays
//! checkable.
//!
//! Run with `cargo run -p turing-engine --example nova_extract` — it
//! compiles (not yet renders) each checkpoint in turn and reports the first
//! one that fails, so the empirical loop this file exists for has a single
//! command to run.

use turing_engine::Page;
use turing_js::compile;

#[path = "common/mod.rs"]
mod common;
use common::PRELUDE;

/// Nova lines 1707-1711. No hooks, no JSX children beyond a text
/// expression — the smallest real leaf component in the file.
const FAV: &str = r#"
function Fav({ f, size }) {
    const s = size || 15;
    const ff = f || {};
    return <div className="fav" style={{ width: s, height: s }}>{ff.letter || ""}</div>;
}
"#;

/// Nova lines 1713-1718. Ternary, string member access, nested JSX.
const URL_TEXT: &str = r#"
function UrlText({ url }) {
    const i = url.indexOf("/");
    const dom = i === -1 ? url : url.slice(0, i);
    const path = i === -1 ? "" : url.slice(i);
    return <span className="ttl mono">{dom}<span>{path}</span></span>;
}
"#;

fn try_compile(label: &str, source: &str) -> bool {
    let program = format!("{PRELUDE}{source}");
    match compile(&program) {
        Ok(_) => {
            println!("compile OK   {label}");
            true
        }
        Err(error) => {
            println!("compile FAIL {label}: {error}");
            false
        }
    }
}

/// Compiling only proves the syntax parses — it says nothing about whether
/// the component actually runs correctly. This mounts it into a real page
/// and renders, the same proof standard the rest of this session's work
/// uses: an engine feature is not "done" until something real ran through
/// it.
fn try_render(label: &str, script: &str) -> bool {
    let html = format!("<html><body><script>{PRELUDE}{script}</script></body></html>");
    match Page::load(&html, 400.0).and_then(|page| page.render(400, 100)) {
        Ok(_) => {
            println!("render OK    {label}");
            true
        }
        Err(error) => {
            println!("render FAIL  {label}: {error}");
            false
        }
    }
}

fn main() {
    let mut all_ok = true;
    all_ok &= try_compile("Fav (Nova:1707-1711)", FAV);
    all_ok &= try_compile("UrlText (Nova:1713-1718)", URL_TEXT);

    all_ok &= try_render(
        "Fav mounted",
        &format!("{FAV}__mount(<Fav f={{{{letter: \"A\"}}}} size={{20}} />, documentBody());"),
    );
    all_ok &= try_render(
        "UrlText mounted",
        &format!("{URL_TEXT}__mount(<UrlText url=\"example.com/page\" />, documentBody());"),
    );

    if !all_ok {
        std::process::exit(1);
    }
}
