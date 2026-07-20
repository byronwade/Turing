// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Turing-owned binding of DOM operations into the script capability registry.
//!
//! This is the second half of `WP-011`: the collector was built and wired, and
//! the binding registry existed with nothing registered in it. This registers
//! real operations over a real document.
//!
//! # The property that matters
//!
//! `REQ-AI-001` treats agents as separately identified principals, and the
//! blueprint's reason for a registry rather than direct calls is that a
//! capability which cannot be listed cannot be granted or revoked. That holds
//! only if the callable set and the listed set are the same set. They are: the
//! interpreter resolves every call through [`turing_js::Host::bindings`], so
//! this host cannot expose an operation that auditing would not show, and
//! revoking one takes effect on the next call.
//!
//! # Deliberate limits
//!
//! Read-only, and over primitives. No operation takes or returns a live node.
//!
//! A node reference is an index into the document's arena, which is a different
//! address space from the interpreter's heap. If a node became a script value,
//! the interpreter's tracing would see an index it would be entitled to read as
//! a heap reference — a confusion invisible until a node is held across a
//! collection. Node identity therefore crosses as an `id` string, and making
//! nodes first-class script values is its own work with its own hazards,
//! including the staleness one `turing-input` already had to solve.
//!
//! Read-only for the same reason in the other direction: a mutating operation
//! advances the document epoch, which invalidates any layout a router is
//! holding, and that interaction deserves its own treatment rather than
//! arriving as a side effect of binding a getter.

#![forbid(unsafe_code)]

use turing_dom::Dom;
use turing_gc::Bindings;
use turing_html::{NodeData, NodeId};
use turing_js::{Host, Value};

/// The interface these operations are registered under.
const INTERFACE: &str = "Document";

/// A [`Host`] exposing read-only document operations to script.
#[derive(Debug)]
pub struct DomHost<'dom> {
    dom: &'dom Dom,
    bindings: Bindings,
}

impl<'dom> DomHost<'dom> {
    /// Binds the default operation set over `dom`.
    #[must_use]
    pub fn new(dom: &'dom Dom) -> Self {
        let mut bindings = Bindings::new();
        bindings.register(INTERFACE, "getAttribute", 2);
        bindings.register(INTERFACE, "tagName", 1);
        bindings.register(INTERFACE, "hasElement", 1);
        bindings.register(INTERFACE, "textContent", 1);
        Self { dom, bindings }
    }

    /// Removes an operation, returning whether one was removed.
    ///
    /// Exposed so a caller can hand a script a narrower surface than the
    /// default. Because invocation resolves through the same registry, a
    /// revoked operation is refused on the next call rather than needing a
    /// second enforcement point that could disagree with the first.
    pub fn revoke(&mut self, name: &str) -> bool {
        self.bindings.revoke(INTERFACE, name)
    }

    /// Returns the element with `id`, or a message naming it.
    fn element(&self, id: &str) -> Result<NodeId, String> {
        self.dom
            .document()
            .element_by_id(id)
            .ok_or_else(|| format!("no element has id {id:?}"))
    }
}

impl Host for DomHost<'_> {
    fn bindings(&self) -> &Bindings {
        &self.bindings
    }

    fn invoke(
        &mut self,
        _interface: &str,
        name: &str,
        arguments: &[Value],
    ) -> Result<Value, String> {
        // Arity was checked against the registry before this was called, so
        // indexing here cannot be out of range.
        let first = arguments[0].to_string();
        match name {
            "hasElement" => Ok(Value::Boolean(
                self.dom.document().element_by_id(&first).is_some(),
            )),
            "tagName" => {
                let node = self.element(&first)?;
                self.dom
                    .document()
                    .element_name(node)
                    .map(|tag| Value::String(tag.to_string()))
                    .ok_or_else(|| format!("the node with id {first:?} is not an element"))
            }
            "getAttribute" => {
                let node = self.element(&first)?;
                let attribute = arguments[1].to_string();
                // A missing attribute is `null`, which is what the DOM
                // specifies. `undefined` would be the natural guess and is a
                // different value that script can tell apart.
                Ok(self
                    .dom
                    .document()
                    .attribute_of(node, &attribute)
                    .map_or(Value::Null, |text| Value::String(text.to_string())))
            }
            "textContent" => {
                let node = self.element(&first)?;
                Ok(Value::String(text_of(self.dom, node)))
            }
            other => Err(format!("{other} is registered but not implemented here")),
        }
    }
}

/// Concatenates the text of a node's descendants, in document order.
///
/// Iterative because document depth is attacker-controlled, and a recursive
/// walk over it aborts the process rather than returning an error.
fn text_of(dom: &Dom, node: NodeId) -> String {
    let document = dom.document();
    let mut text = String::new();
    let mut stack = vec![node];
    while let Some(current) = stack.pop() {
        if let NodeData::Text(chunk) = &document.node(current).data {
            text.push_str(chunk);
        }
        // Reversed, because popping visits the last push first and text must
        // read in document order.
        stack.extend(document.node(current).children.iter().rev().copied());
    }
    text
}
