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

/// Nova lines 1707-1711. Adaptations: none — byte-for-byte the source
/// lines (object destructuring, default parameters, and the object-spread
/// merge in `style` all run as real engine features now).
const FAV: &str = r#"
function Fav({ f, size }) {
    const s = size || 15;
    const ff = f || {};
    return <div className="fav" style={{ ...(ff.style || { background: "var(--c4)" }), width: s, height: s }}>{ff.letter || ""}</div>;
}
"#;

/// Nova lines 1713-1718. Adaptations: none — byte-for-byte the source
/// lines (ternary, string member access, nested JSX, and both `style`
/// props; the first extraction of this component had dropped both
/// `style` props since plain object literals alone were enough to
/// compile — a silent simplification, fixed once nothing needed
/// simplifying to pass).
const URL_TEXT: &str = r#"
function UrlText({ url }) {
    const i = url.indexOf("/");
    const dom = i === -1 ? url : url.slice(0, i);
    const path = i === -1 ? "" : url.slice(i);
    return <span className="ttl mono" style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{dom}<span style={{ color: "var(--tx2)" }}>{path}</span></span>;
}
"#;

/// NOT a full Nova component — a deliberately narrow, honestly-labeled
/// extraction of just the `style` pattern real Nova's `HRow` uses at line
/// 1815: `style={{ transform: `translateY(${y}px)` }}`, the most common
/// template-literal shape in the file (a single numeric interpolation
/// inside a CSS function-notation string). `HRow` itself (lines 1813-1824)
/// also needs `memo()`, a *named* function expression (`function
/// HRow(...)`, still refused — `memo()`'s own argument shape, not
/// `HRow`-specific), inline-arrow `onClick` handlers (the per-call-fresh-
/// heap problem: a handler capturing render-local state cannot survive to
/// a later dispatch, unlike a bare top-level function reference), and
/// `aria-label`/other non-`className` attributes `__applyProps` does not
/// forward. None of those are ready. Adaptations from the cited line:
/// wrapped in a synthetic component name and reduced to just the `style`
/// prop, since extracting the whole thing now would mean silently
/// dropping the rest — the mistake this harness exists to catch, not
/// repeat. `HRow` itself stays on the not-yet-extracted list until its
/// other prerequisites land.
const TRANSLATE_Y_STYLE_PATTERN: &str = r#"
function TranslateYRow({ y }) {
    return <div className="hrow" style={{ transform: `translateY(${y}px)` }} />;
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
    all_ok &= try_compile(
        "TranslateYRow pattern (Nova:1815)",
        TRANSLATE_Y_STYLE_PATTERN,
    );

    all_ok &= try_render(
        "Fav mounted",
        &format!("{FAV}__mount(<Fav f={{{{letter: \"A\"}}}} size={{20}} />, documentBody());"),
    );
    all_ok &= try_render(
        "UrlText mounted",
        &format!("{URL_TEXT}__mount(<UrlText url=\"example.com/page\" />, documentBody());"),
    );
    all_ok &= try_render(
        "TranslateYRow pattern mounted",
        &format!("{TRANSLATE_Y_STYLE_PATTERN}__mount(<TranslateYRow y={{42}} />, documentBody());"),
    );

    if !all_ok {
        std::process::exit(1);
    }
}
