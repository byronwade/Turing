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
//! # Node handles
//!
//! The read/query operations address elements by `id` string. The
//! construction operations — `createElement`, `createText`, `appendChild`,
//! `setNodeAttribute`, `documentBody` — address nodes by an **opaque numeric
//! handle**: a `Number` equal to the node's arena index.
//!
//! This handle is deliberately not a live node and not a heap reference. It is
//! a plain integer the interpreter's tracing treats as a number, never as a
//! pointer, so the address-space confusion that made live nodes hazardous
//! cannot arise — a handle held across a collection is still just a number.
//! The index is stable because construction only appends to the arena; nodes
//! are never removed or reindexed here, so a handle cannot come to denote a
//! different node. A handle to a node that does not exist fails on use rather
//! than reading a neighbour — but not because `turing_html` checks; its
//! `NodeId`-indexed access is raw and panics out of range, which is a
//! reasonable closed-world contract for an id the engine minted itself. The
//! check belongs to, and lives entirely in, [`node_handle`] below: it is the
//! one seam an arbitrary script number becomes a `NodeId`, so it is the one
//! place that validates the number is actually in range before that
//! conversion happens.
//!
//! This is the renderer's vocabulary. React's host configuration is exactly
//! `createElement` / `createTextNode` / `appendChild` / `setAttribute` over
//! opaque host handles, which is why these five operations are the DOM step of
//! the application-runtime ladder (`docs/application-runtime/README.md`).
//!
//! # Mutation and invalidation
//!
//! Attribute mutation is bound, and it is the reason the epoch exists. A
//! mutating operation advances the document's epoch, which invalidates any
//! layout computed before it — a `turing_input::HitRouter` built earlier will
//! refuse to route rather than deliver an event against geometry that no longer
//! describes the document.
//!
//! That invalidation is not implemented here. It falls out of `turing-dom`
//! advancing the epoch and `turing-input` checking it, which is the point: an
//! embedder cannot bind a mutation that forgets to invalidate, because the
//! binding does not carry the responsibility.
//!
//! A refused mutation does not advance the epoch. That is load-bearing rather
//! than incidental: if it did, a script probing for elements that do not exist
//! would invalidate every cached layout in the process.

#![forbid(unsafe_code)]

use turing_dom::Dom;
use turing_gc::Bindings;
use turing_html::{NodeData, NodeId};
use turing_js::{Host, Value};

/// The interface these operations are registered under.
const INTERFACE: &str = "Document";

/// Operations that can change the document.
///
/// Named in one place so [`DomHost::read_only`] cannot fall behind the set
/// [`DomHost::new`] registers: adding a mutator without adding it here would
/// silently widen the read-only surface, which is the direction that matters.
// `addEventListener` mutates no tree node, but it changes what future
// dispatches do, which is a document-behaviour mutation; a read-only
// principal must not get it.
const MUTATING_OPERATIONS: &[&str] = &[
    "setAttribute",
    "removeAttribute",
    "addEventListener",
    "createElement",
    "createText",
    "appendChild",
    "setNodeAttribute",
    "insertBefore",
    "removeChild",
];

/// A [`Host`] exposing read-only document operations to script.
#[derive(Debug)]
pub struct DomHost<'dom> {
    dom: &'dom mut Dom,
    bindings: Bindings,
}

impl<'dom> DomHost<'dom> {
    /// Binds the default operation set over `dom`, reads and writes both.
    #[must_use]
    pub fn new(dom: &'dom mut Dom) -> Self {
        let mut bindings = Bindings::new();
        bindings.register(INTERFACE, "getAttribute", 2);
        bindings.register(INTERFACE, "tagName", 1);
        bindings.register(INTERFACE, "hasElement", 1);
        bindings.register(INTERFACE, "textContent", 1);
        bindings.register(INTERFACE, "setAttribute", 3);
        bindings.register(INTERFACE, "removeAttribute", 2);
        bindings.register(INTERFACE, "addEventListener", 3);
        // Construction operations. A node created or located by these crosses
        // into script as an opaque numeric handle — its arena index — which is
        // stable because construction only appends. This is the renderer's
        // vocabulary: React's host config is createElement/createTextNode/
        // appendChild/setAttribute over exactly such handles.
        bindings.register(INTERFACE, "documentBody", 0);
        bindings.register(INTERFACE, "createElement", 1);
        bindings.register(INTERFACE, "createText", 1);
        bindings.register(INTERFACE, "appendChild", 2);
        bindings.register(INTERFACE, "setNodeAttribute", 3);
        // Update and navigation operations: a reconciler does not only mount,
        // it moves, replaces, and removes, and it reads the current tree to
        // decide. These are the patch half of the renderer's vocabulary.
        bindings.register(INTERFACE, "insertBefore", 3);
        bindings.register(INTERFACE, "removeChild", 1);
        bindings.register(INTERFACE, "parentNode", 1);
        bindings.register(INTERFACE, "firstChild", 1);
        Self { dom, bindings }
    }

    /// Binds only the operations that cannot change the document.
    ///
    /// The narrower surface a caller would hand an untrusted principal. Built by
    /// revoking from the default rather than by a second registration list,
    /// because two lists drift and the one that drifts is the restrictive one.
    #[must_use]
    pub fn read_only(dom: &'dom mut Dom) -> Self {
        let mut host = Self::new(dom);
        for name in MUTATING_OPERATIONS {
            host.revoke(name);
        }
        host
    }

    /// Returns the document, so a caller can observe what script did.
    #[must_use]
    pub fn dom(&self) -> &Dom {
        self.dom
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

/// Reads a script value used as a node handle back into a [`NodeId`],
/// validated against `dom`'s current arena.
///
/// A handle crosses into script as a `Number` equal to the arena index, and
/// script can write any number literal it likes — `appendChild(999999999,
/// 0)` is ordinary, not exploitation, and the interpreter has no way to stop
/// a script writing it. Every internal consumer of a [`NodeId`] indexes the
/// arena directly and trusts the id is in range, which is a reasonable
/// closed-world contract for ids the engine minted itself but is exactly
/// wrong for one script handed back to it. So the check belongs here, at the
/// one seam where an arbitrary script number becomes a `NodeId`: out of range
/// is refused with a typed message, not handed downstream to panic on.
fn node_handle(dom: &Dom, value: &Value) -> Result<NodeId, String> {
    let Value::Number(index) = value else {
        return Err(format!("expected a node handle, got {value}"));
    };
    if *index < 0.0 || index.fract() != 0.0 {
        return Err(format!("{index} is not a node handle"));
    }
    #[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
    let index = *index as usize;
    if index >= dom.document().len() {
        return Err(format!(
            "{index} is not a live node handle; the document has {} nodes",
            dom.document().len()
        ));
    }
    Ok(NodeId::from_index(index))
}

/// The arena index of a node, as the `Number` script sees.
fn node_value(node: NodeId) -> Value {
    #[allow(clippy::cast_precision_loss)]
    Value::Number(node.index() as f64)
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
        // Arity was checked against the registry before this was called. The
        // id-based operations read `arguments[0]` as an id string; the
        // construction operations read handles, so `first` is computed only
        // where an id is what the operation takes.
        let first = || arguments[0].to_string();
        match name {
            "documentBody" => Ok(document_body(self.dom).map_or(Value::Null, node_value)),
            "createElement" => {
                let handle = self
                    .dom
                    .create_element(&first())
                    .map_err(|error| error.to_string())?;
                Ok(node_value(handle.node()))
            }
            "createText" => {
                let handle = self.dom.create_text(&first());
                Ok(node_value(handle.node()))
            }
            "appendChild" => {
                let parent = self.dom.handle(node_handle(self.dom, &arguments[0])?);
                let child = self.dom.handle(node_handle(self.dom, &arguments[1])?);
                self.dom
                    .append_child(parent, child)
                    .map_err(|error| error.to_string())?;
                Ok(Value::Undefined)
            }
            "setNodeAttribute" => {
                let node = self.dom.handle(node_handle(self.dom, &arguments[0])?);
                let name = arguments[1].to_string();
                let value = arguments[2].to_string();
                self.dom
                    .set_attribute(node, &name, &value)
                    .map_err(|error| error.to_string())?;
                Ok(Value::Undefined)
            }
            "insertBefore" => {
                // insertBefore(parent, child, reference): place `child` before
                // `reference` among `parent`'s children.
                let parent = self.dom.handle(node_handle(self.dom, &arguments[0])?);
                let child = self.dom.handle(node_handle(self.dom, &arguments[1])?);
                let reference = self.dom.handle(node_handle(self.dom, &arguments[2])?);
                self.dom
                    .insert_before(parent, child, reference)
                    .map_err(|error| error.to_string())?;
                Ok(Value::Undefined)
            }
            "removeChild" => {
                let child = self.dom.handle(node_handle(self.dom, &arguments[0])?);
                self.dom
                    .remove_child(child)
                    .map_err(|error| error.to_string())?;
                Ok(Value::Undefined)
            }
            "parentNode" => {
                let node = node_handle(self.dom, &arguments[0])?;
                // `null` for a node with no parent, which is what the DOM
                // returns and is distinguishable from a handle.
                Ok(self
                    .dom
                    .document()
                    .node(node)
                    .parent
                    .map_or(Value::Null, node_value))
            }
            "firstChild" => {
                let node = node_handle(self.dom, &arguments[0])?;
                Ok(self
                    .dom
                    .document()
                    .node(node)
                    .children
                    .first()
                    .copied()
                    .map_or(Value::Null, node_value))
            }
            "hasElement" => Ok(Value::Boolean(
                self.dom.document().element_by_id(&first()).is_some(),
            )),
            "tagName" => {
                let node = self.element(&first())?;
                self.dom
                    .document()
                    .element_name(node)
                    .map(|tag| Value::String(tag.to_string()))
                    .ok_or_else(|| format!("the node with id {:?} is not an element", first()))
            }
            "getAttribute" => {
                let node = self.element(&first())?;
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
                let node = self.element(&first())?;
                Ok(Value::String(text_of(self.dom, node)))
            }
            "setAttribute" => {
                let node = self.element(&first())?;
                let handle = self.dom.handle(node);
                let name = arguments[1].to_string();
                let value = arguments[2].to_string();
                self.dom
                    .set_attribute(handle, &name, &value)
                    .map_err(|error| error.to_string())?;
                // Nothing useful to return, and `undefined` is what the DOM
                // gives back from a setter.
                Ok(Value::Undefined)
            }
            "removeAttribute" => {
                let node = self.element(&first())?;
                let handle = self.dom.handle(node);
                let name = arguments[1].to_string();
                self.dom
                    .remove_attribute(handle, &name)
                    .map_err(|error| error.to_string())?;
                Ok(Value::Undefined)
            }
            "addEventListener" => {
                // `addEventListener(id, kind, functionName)`. The listener is
                // registered in the DOM's own dispatch machinery with the
                // function's name as its identifier and no declarative
                // effects; whoever owns the interpreter maps the reported
                // invocation back to the named function and calls it. This
                // keeps propagation order the DOM's business and execution
                // the embedder's, with the invocation record as the seam.
                let node = self.element(&first())?;
                let handle = self.dom.handle(node);
                let kind = arguments[1].to_string();
                let function = arguments[2].to_string();
                self.dom
                    .add_listener(handle, &kind, &function, false, &[])
                    .map_err(|error| error.to_string())?;
                Ok(Value::Undefined)
            }
            other => Err(format!("{other} is registered but not implemented here")),
        }
    }
}

/// Concatenates the text of a node's descendants, in document order.
///
/// Iterative because document depth is attacker-controlled, and a recursive
/// walk over it aborts the process rather than returning an error.
/// The `<body>` element's node, or the first element if the document has no
/// body, or `None` for an empty document. This is the attachment point a
/// script builds its subtree under.
fn document_body(dom: &Dom) -> Option<NodeId> {
    let document = dom.document();
    let mut first_element = None;
    for index in 0..document.len() {
        let node = NodeId::from_index(index);
        if let Some(name) = document.element_name(node) {
            if name == "body" {
                return Some(node);
            }
            first_element.get_or_insert(node);
        }
    }
    first_element
}

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
