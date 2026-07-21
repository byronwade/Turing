// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Shared JSX reconciler prelude for engine examples that render `turing-js`
//! JSX through the real DOM/layout/paint pipeline. Factored out of
//! `jsx_demo.rs` so `nova_extract.rs` (and any later example doing the same
//! kind of walkthrough) shares one definition instead of a copy each could
//! drift from.

use turing_raster::Canvas;

/// Resolves a `createElement`-built value into real DOM nodes under
/// `parentHandle`, recursing into component functions until only host
/// (string-tagged) elements and text/falsy leaves remain.
///
/// JS, not Rust, because the VM's heap is fresh on every separate call into
/// it — a `createElement` result returned from one call would be a
/// reference into a heap already gone by the time a second, Rust-side call
/// tried to read it. Staying inside one JS call for the whole walk avoids
/// that entirely: nested component calls are just JS calling JS in the
/// still-live heap.
pub(crate) const PRELUDE: &str = r#"
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

#[allow(dead_code)]
pub(crate) fn write_bmp(canvas: &Canvas, path: &str) -> std::io::Result<()> {
    std::fs::write(path, turing_raster::encode_bmp(canvas))
}
