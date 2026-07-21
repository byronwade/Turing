// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! First real, verified JSX-to-pixels walkthrough: hand-authored JSX
//! components — not the 7,727-line Nova design source, which
//! `docs/ui-runtime/design-lab/README.md` documents as a visual reference to
//! be *extracted* from (tokens, layout, component states), never executed
//! directly (it imports the real `react`/`lucide-react` npm packages, and
//! its own README forbids React/webview in trusted chrome) — compiled by
//! `turing-js`'s real JSX parser, resolved by a JS-authored reconciler
//! (`__jsxCreateElement` + `__mount`, prepended as a prelude) into real DOM
//! nodes via the existing
//! `createElement`/`createText`/`appendChild`/`setNodeAttribute` host
//! operations, laid out and painted by the real engine pipeline.
//!
//! Two checkpoints in one run: a stateless render (proves the
//! createElement→DOM bridge end to end), then a real, host-persisted
//! `useState` hook driven by an actual simulated click through
//! `Page::dispatch_at` (proves the interactive hooks loop: click → setState
//! → full remount → visibly different pixels).
//!
//! Run with `cargo run -p turing-engine --example jsx_demo -- out` to write
//! `out-1-stateless.bmp` and `out-2-before.bmp`/`out-2-after.bmp`.

use std::env;
use std::process::ExitCode;

use turing_engine::Page;
use turing_raster::{Canvas, encode_bmp};

/// The reconciler: resolves a `createElement`-built value into real DOM
/// nodes under `parentHandle`, recursing into component functions until
/// only host (string-tagged) elements and text/falsy leaves remain.
///
/// JS, not Rust, because the VM's heap is fresh on every separate call into
/// it — a `createElement` result returned from one call would be a
/// reference into a heap already gone by the time a second, Rust-side call
/// tried to read it. Staying inside one JS call for the whole walk avoids
/// that entirely: nested component calls are just JS calling JS in the
/// still-live heap.
const PRELUDE: &str = r#"
function __jsxCreateElement(type, props, children) {
    return { type: type, props: props, children: children };
}

function __applyProps(handle, props) {
    if (valueKind(props) != "object") { return; }
    if (valueKind(props.className) == "string") {
        setNodeAttribute(handle, "class", props.className);
    }
    if (valueKind(props.onClick) == "string") {
        var elementId = "jsx-" + handle;
        setNodeAttribute(handle, "id", elementId);
        addEventListener(elementId, "click", props.onClick);
    }
}

function __mount(vnode, parentHandle) {
    var kind = valueKind(vnode);
    if (kind == "string" || kind == "number") {
        appendChild(parentHandle, createText(vnode));
        return;
    }
    if (kind != "object") {
        // undefined / null / boolean / function-as-a-bare-child: all the
        // falsy sentinels real JSX drops rather than renders, and anything
        // else unrecognised is likewise dropped rather than guessed at.
        return;
    }
    var typeKind = valueKind(vnode.type);
    if (typeKind == "function") {
        var rendered = vnode.type(vnode.props);
        __mount(rendered, parentHandle);
        return;
    }
    var handle = createElement(vnode.type);
    // Attached to the document *before* props/children, not after: an
    // `onClick` prop needs `addEventListener`, which looks the element up
    // by its "id" attribute against the live document tree — a handle that
    // exists but is not yet reachable from the document has no id lookup
    // can find yet.
    appendChild(parentHandle, handle);
    __applyProps(handle, vnode.props);
    var children = vnode.children;
    var i = 0;
    while (i < children.length) {
        __mount(children[i], handle);
        i = i + 1;
    }
}

function __unmountChildren(parentHandle) {
    var child = firstChild(parentHandle);
    while (valueKind(child) == "number") {
        removeChild(child);
        child = firstChild(parentHandle);
    }
}
"#;

/// Checkpoint 1: a stateless component tree — nested host elements, text,
/// an expression child, and one nested custom component (`Badge`) — proving
/// the whole bridge (JSX parse → `__jsxCreateElement` → `__mount` → real DOM
/// → layout → paint) with nothing hook-related in the way yet.
///
/// `Badge` and `App` are real top-level sibling declarations, referenced
/// from JSX (`<Badge .../>`, `<App />`) exactly the way idiomatic
/// component code is written. A JSX uppercase tag desugars to
/// `Expr::Variable`, and that now falls through — after the usual local and
/// captured-upvalue checks fail — to a global table every top-level
/// `function`/`const`/`let` is hoisted into, reachable from a function body
/// at any nesting depth. Earlier this had to be worked around by nesting
/// both components as locals of `__turingRenderRoot`, since a bare
/// reference to a sibling top-level declaration had nowhere to resolve to;
/// that workaround is gone now that the global table exists.
const STATELESS_DEMO: &str = r#"
function Badge(props) {
    return <span className="badge">{props.label}</span>;
}

function App(props) {
    return (
        <div className="card">
            <span className="title">Turing renders JSX</span>
            <Badge label="real pipeline" />
        </div>
    );
}

function __turingRenderRoot() {
    __unmountChildren(documentBody());
    __mount(<App />, documentBody());
}

__turingRenderRoot();
"#;

/// Checkpoint 2: a real `useState`-shaped counter. `useState` here is a
/// direct native pair (`__hookState`/`__hookSet`) rather than the
/// index-closure trick real React uses internally, because a handler
/// function is looked up *by name* at dispatch time (`addEventListener`'s
/// own convention) long after the render call that would have created any
/// such closure has already ended and dropped its heap — so the handler is
/// an ordinary named top-level function, and it names its own state slot
/// directly. The value each slot holds is host-persisted (outside the VM's
/// per-call heap) and restricted to primitives — an object/array/closure
/// value would be a dangling heap reference by the next call, so storing
/// one is refused rather than silently corrupted.
const STATEFUL_DEMO: &str = r#"
function Counter(props) {
    var count = __hookState(0, 0);
    return (
        <div className="card">
            <span className="title">Count: {count}</span>
            <button className="button" onClick="handleIncrement">+1</button>
        </div>
    );
}

function __turingRenderRoot() {
    __unmountChildren(documentBody());
    __mount(<Counter />, documentBody());
}

function handleIncrement() {
    __hookSet(0, __hookState(0, 0) + 1);
    __turingRenderRoot();
}

__turingRenderRoot();
"#;

const STYLE: &str = r#"
<style>
.card { display: block; background: #1e293b; padding: 16px; border: 2px; border-color: #38bdf8; }
.title { display: block; color: #f8fafc; }
.badge { display: block; background: #38bdf8; color: #0f172a; padding: 4px; }
.button { display: block; background: #22c55e; color: #0f172a; padding: 8px; }
</style>
"#;

fn write_bmp(canvas: &Canvas, path: &str) -> std::io::Result<()> {
    std::fs::write(path, encode_bmp(canvas))
}

fn run() -> Result<(), String> {
    let out_prefix = env::args().nth(1).unwrap_or_else(|| "jsx_demo".to_string());

    // -- Checkpoint 1: stateless -------------------------------------------
    let html = format!(
        "<html><head>{STYLE}</head><body><script>{PRELUDE}{STATELESS_DEMO}</script></body></html>"
    );
    let page = Page::load(&html, 400.0).map_err(|error| format!("checkpoint 1: {error}"))?;
    let canvas = page
        .render(400, 200)
        .map_err(|error| format!("checkpoint 1 render: {error}"))?;
    write_bmp(&canvas, &format!("{out_prefix}-1-stateless.bmp"))
        .map_err(|error| format!("checkpoint 1 write: {error}"))?;
    println!("checkpoint 1 (stateless): {out_prefix}-1-stateless.bmp");

    // -- Checkpoint 2: stateful, real click ---------------------------------
    let html = format!(
        "<html><head>{STYLE}</head><body><script>{PRELUDE}{STATEFUL_DEMO}</script></body></html>"
    );
    let mut page = Page::load(&html, 400.0).map_err(|error| format!("checkpoint 2: {error}"))?;
    let before = page
        .render(400, 200)
        .map_err(|error| format!("checkpoint 2 before-render: {error}"))?;
    write_bmp(&before, &format!("{out_prefix}-2-before.bmp"))
        .map_err(|error| format!("checkpoint 2 write: {error}"))?;
    println!("checkpoint 2 before click: {out_prefix}-2-before.bmp");

    // A real simulated click, through the same `Page::dispatch_at` path any
    // embedder's input pipeline would use — not a direct call into the
    // handler bypassing hit testing.
    let point = turing_layout::Point { x: 40.0, y: 46.0 };
    let hit = page
        .target_at(point)
        .map_err(|error| format!("checkpoint 2 hit test: {error}"))?
        .ok_or("checkpoint 2: the click point did not land on the button")?;
    let hit_tag = page.dom().document().element_name(hit);
    if hit_tag != Some("button") {
        return Err(format!(
            "checkpoint 2: expected the click to hit the button, hit {hit_tag:?} instead"
        ));
    }
    let dispatch = page
        .dispatch_at(point, &turing_dom::Event::new("click"))
        .map_err(|error| format!("checkpoint 2 dispatch: {error}"))?
        .ok_or("checkpoint 2: dispatch reported no hit despite target_at finding one")?;
    let listeners: Vec<String> = dispatch
        .invocations
        .iter()
        .map(|invocation| invocation.listener.clone())
        .collect();
    if listeners != ["handleIncrement"] {
        return Err(format!(
            "checkpoint 2: expected exactly [\"handleIncrement\"] to run, got {listeners:?}"
        ));
    }
    println!("checkpoint 2 click ran: {listeners:?}");

    let after = page
        .render(400, 200)
        .map_err(|error| format!("checkpoint 2 after-render: {error}"))?;
    write_bmp(&after, &format!("{out_prefix}-2-after.bmp"))
        .map_err(|error| format!("checkpoint 2 write: {error}"))?;
    println!("checkpoint 2 after click: {out_prefix}-2-after.bmp");

    // A genuine pixel scan, not a hand-picked sample point: proves the
    // click's host-persisted state update actually reached a fresh render
    // that painted differently, without depending on knowing in advance
    // exactly where in the canvas the changed glyph lands.
    let differing_pixels = (0..200)
        .flat_map(|y| (0..400).map(move |x| (x, y)))
        .filter(|&(x, y)| before.pixel(x, y) != after.pixel(x, y))
        .count();
    println!("checkpoint 2: {differing_pixels} pixels changed after the click");
    if differing_pixels == 0 {
        return Err(
            "checkpoint 2: the click's state update produced no visible pixel change".to_string(),
        );
    }

    Ok(())
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("jsx_demo: {error}");
            ExitCode::FAILURE
        }
    }
}
