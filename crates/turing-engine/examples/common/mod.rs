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
// Real React's `memo()` only changes whether a re-render is *skipped* when
// props are unchanged — it never changes what a first render produces,
// and this reconciler does not memoize renders at all yet (every call to
// `__mount` walks the whole tree). An identity shim is therefore
// output-preserving, not a simplification: it keeps `memo(fn)`-wrapped
// Nova components extractable verbatim instead of needing `memo(...)`
// stripped out of the cited source at each one.
function memo(component) {
    return component;
}

// Milestone 1 of the React-runtime plan (see the turing-nova-source-real-
// scope project memory): a single, non-interactive static first paint.
// Every VM call gets a fresh heap, so nothing here needs to persist a
// render's state to the next one yet -- these hooks are correct for a
// *first* render only, by construction, not an approximation:
//   - useState returns the initial value and a setter that does nothing.
//     Real React's setter schedules a re-render; there is no re-render
//     loop yet for it to schedule into, so a no-op is the honest behavior
//     for this milestone, not a wrong one.
//   - useRef returns a plain, real {current} object -- genuinely correct,
//     not a stand-in, since a ref's identity persisting across renders
//     only matters once there are multiple renders.
//   - useCallback/useMemo return their function/computed value directly:
//     memoization across renders is meaningless when there is only one.
//   - useEffect/useLayoutEffect do not run their callback at all. Real
//     effects fire after paint and exist to wire up interactivity
//     (subscriptions, measurements, event listeners) -- none of that is
//     first-paint content, so skipping them is correct for this
//     milestone's output, not a gap in it.
function useState(initial) {
    return [initial, function (next) {}];
}
function useRef(initial) {
    return { current: initial };
}
function useCallback(fn, deps) {
    return fn;
}
function useMemo(fn, deps) {
    return fn();
}
function useEffect(fn, deps) {}
function useLayoutEffect(fn, deps) {}

// What `<>...</>` desugars to referencing by name (see the module-level
// JSX doc comment in turing-js). A real Fragment's job is "render my
// children with no wrapping element at all" -- `__mount` below is what
// actually needs to know how to do that when it meets a Fragment-typed
// vnode, not this function itself.
function Fragment(props) {
    return props.children;
}

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
    if (kind == "array") {
        // A component (Fragment, or any other returning a bare list) that
        // rendered to a list of children rather than one wrapping element
        // -- mount each in turn under the same parent, exactly the way
        // real React flattens a Fragment's children into its parent.
        var i = 0;
        while (i < vnode.length) {
            __mount(vnode[i], parentHandle);
            i = i + 1;
        }
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
