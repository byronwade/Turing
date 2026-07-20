// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Turing-owned DOM mutation epochs and event dispatch.
//!
//! This crate implements `WP-007` and `REQ-ENG-002`: a live document that can
//! be mutated, with the epoch discipline the rest of the system relies on, and
//! the three-phase event dispatch model. It is written from the DOM standard
//! and derives from no existing engine, consistent with `ADR-0009` Option A.
//!
//! # Why epochs are here rather than in `turing-html`
//!
//! `turing-html` owns tree *structure*. This crate owns tree *liveness*. Every
//! structural mutation advances a [`Epoch`], and a [`Handle`] captures the
//! epoch it was obtained at. Acting through a handle taken before a mutation
//! fails with [`DomError::StaleHandle`] rather than silently addressing
//! whatever now occupies that slot.
//!
//! That is not defensive programming for its own sake. The architecture
//! prototype already carries a document epoch through IPC and agent
//! authorization, and `REQ-AI-003` requires that every agent action validate
//! the document epoch. An agent that reads the page, pauses, and then clicks
//! must not act on a node index that now means something else. Stale-handle
//! rejection is where that requirement becomes executable.
//!
//! # Deliberate limits
//!
//! Implemented: element and text creation, append, insert-before, removal,
//! attribute setting and removal, cycle rejection, epoch invalidation, and
//! capture/target/bubble dispatch with `stopPropagation`,
//! `stopImmediatePropagation`, and `preventDefault`.
//!
//! Not implemented, each returning a typed error rather than an approximation:
//!
//! - shadow trees, which retarget events and change the propagation path;
//! - custom element reactions, which run author code at defined points during
//!   mutation;
//! - `MutationObserver`, whose delivery is ordered against microtask timing
//!   this crate has no scheduler for.
//!
//! Each of these changes observable ordering or the event path. Approximating
//! one would make listener behaviour disagree with every other engine in ways
//! that surface as intermittent bugs rather than obvious failures.

#![forbid(unsafe_code)]

use core::fmt;
use turing_html::{Attribute, Document, MutationError, NodeData, NodeId};

/// A monotonically increasing document version.
///
/// Advanced by every structural mutation. Attribute changes advance it too,
/// because a selector match can depend on an attribute.
#[derive(Clone, Copy, Debug, Default, Eq, Ord, PartialEq, PartialOrd)]
pub struct Epoch(u64);

impl Epoch {
    /// Returns the raw counter, for recording in IPC or evidence.
    #[must_use]
    pub const fn value(self) -> u64 {
        self.0
    }

    /// Rebuilds an epoch from a counter recorded earlier.
    #[must_use]
    pub const fn from_value(value: u64) -> Self {
        Self(value)
    }
}

impl fmt::Display for Epoch {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "epoch {}", self.0)
    }
}

/// A node reference bound to the epoch it was taken at.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Handle {
    node: NodeId,
    epoch: Epoch,
}

impl Handle {
    /// Returns the node this handle refers to, without checking staleness.
    ///
    /// Prefer passing the handle to a [`Dom`] method, which validates first.
    #[must_use]
    pub const fn node(self) -> NodeId {
        self.node
    }

    /// Returns the epoch this handle was taken at.
    #[must_use]
    pub const fn epoch(self) -> Epoch {
        self.epoch
    }
}

/// A DOM operation that was refused.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum DomError {
    /// The handle predates a mutation, so the node it names may have changed.
    StaleHandle { handle: Epoch, current: Epoch },
    /// The tree refused the structural change.
    Mutation(MutationError),
    /// Shadow trees retarget events and change the propagation path.
    ShadowTreeUnsupported,
    /// Custom element reactions run author code during mutation.
    CustomElementUnsupported { name: String },
    /// `MutationObserver` delivery is ordered against microtask timing.
    MutationObserverUnsupported,
    /// The requested change history is outside what the document retains.
    ChangesUnavailable {
        requested: Epoch,
        oldest: Epoch,
        current: Epoch,
    },
}

impl From<MutationError> for DomError {
    fn from(error: MutationError) -> Self {
        Self::Mutation(error)
    }
}

impl fmt::Display for DomError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::StaleHandle { handle, current } => write!(
                formatter,
                "refused: handle taken at {handle} but the document is now at {current}"
            ),
            Self::Mutation(error) => write!(formatter, "{error}"),
            Self::ShadowTreeUnsupported => write!(
                formatter,
                "shadow trees are not implemented; they retarget events and change the propagation path"
            ),
            Self::CustomElementUnsupported { name } => write!(
                formatter,
                "custom element <{name}> is not implemented; its reactions run author code during mutation"
            ),
            Self::MutationObserverUnsupported => write!(
                formatter,
                "MutationObserver is not implemented; its delivery depends on microtask ordering"
            ),
            Self::ChangesUnavailable {
                requested,
                oldest,
                current,
            } => write!(
                formatter,
                "the change history from epoch {} is not available: the document                  retains from {} and is now at {}. Answering with what remains                  would understate what changed, and a caller would act on it as                  though it were complete",
                requested.value(),
                oldest.value(),
                current.value()
            ),
        }
    }
}

/// The phase of dispatch a listener was invoked in.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Phase {
    /// Walking down from the root toward the target.
    Capturing,
    /// At the target itself.
    AtTarget,
    /// Walking back up from the target.
    Bubbling,
}

/// What one mutation changed.
///
/// The blueprint requires the engine to record which nodes a stage affected,
/// not merely that something happened. An epoch alone says a document moved on;
/// this says what moved.
///
/// Deliberately coarse. A consumer learns which node and which kind of change,
/// not the old and new values: keeping values would mean retaining a copy of
/// every string a page ever set, and nothing that consumes this needs them.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum Change {
    /// A node was created. It is detached until inserted.
    NodeCreated { node: NodeId },
    /// A parent's child list changed by insertion or removal.
    ChildList { parent: NodeId },
    /// An attribute was set or removed on an element.
    Attribute { node: NodeId, name: String },
}

/// How many changes a document retains.
///
/// The log is attacker-influenced — a script mutates in a loop — so it is
/// bounded like every other growth path in this workspace. Past the bound the
/// oldest entries are dropped and a query reaching back that far is refused
/// rather than answered with what happens to remain: a partial answer
/// understates what changed, and a consumer would act on it as though it were
/// complete.
pub const MAX_RECORDED_CHANGES: usize = 4096;

/// A dispatched event.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Event {
    /// Event type, such as `click`.
    pub kind: String,
    /// Whether the event bubbles after reaching the target.
    pub bubbles: bool,
    /// Whether `preventDefault` has an effect.
    pub cancelable: bool,
}

impl Event {
    /// Creates a bubbling, cancelable event, matching common UI events.
    #[must_use]
    pub fn new(kind: &str) -> Self {
        Self {
            kind: kind.to_string(),
            bubbles: true,
            cancelable: true,
        }
    }

    /// Creates a non-bubbling event, matching events such as `focus`.
    #[must_use]
    pub fn non_bubbling(kind: &str) -> Self {
        Self {
            kind: kind.to_string(),
            bubbles: false,
            cancelable: true,
        }
    }
}

/// One listener invocation, recorded in dispatch order.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Invocation {
    /// The node whose listener ran.
    pub node: NodeId,
    /// Listener identifier supplied at registration.
    pub listener: String,
    /// Phase the listener ran in.
    pub phase: Phase,
}

/// The outcome of dispatching an event.
#[derive(Clone, Debug, Default, Eq, PartialEq)]
pub struct Dispatch {
    /// Listener invocations in the order they ran.
    pub invocations: Vec<Invocation>,
    /// Whether `preventDefault` was called by any listener that ran.
    pub default_prevented: bool,
}

/// A registered listener.
#[derive(Clone, Debug, Eq, PartialEq)]
struct Listener {
    node: NodeId,
    kind: String,
    name: String,
    capture: bool,
    /// Actions the listener performs when it runs.
    effects: Vec<Effect>,
}

/// What a listener does when invoked.
///
/// Real listeners run script. Until `WP-010` provides an interpreter, a
/// listener declares its propagation effects directly, which is enough to
/// exercise and pin the dispatch algorithm.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Effect {
    /// Stop propagation after the current node finishes.
    StopPropagation,
    /// Stop immediately, skipping later listeners on this same node.
    StopImmediatePropagation,
    /// Mark the event's default action as prevented.
    PreventDefault,
}

/// A live document with epoch tracking and event dispatch.
#[derive(Debug)]
pub struct Dom {
    document: Document,
    /// Changes in the order they happened, most recent last.
    changes: std::collections::VecDeque<Change>,
    /// The epoch the oldest retained change advanced the document *to*.
    ///
    /// Queries older than this are refused, because the entries that would
    /// answer them have been dropped.
    oldest_retained: Epoch,
    epoch: Epoch,
    listeners: Vec<Listener>,
}

impl Dom {
    /// Wraps a parsed document.
    #[must_use]
    pub fn new(document: Document) -> Self {
        Self {
            document,
            epoch: Epoch::default(),
            listeners: Vec::new(),
            changes: std::collections::VecDeque::new(),
            oldest_retained: Epoch::default(),
        }
    }

    /// Returns the underlying document for reading.
    #[must_use]
    pub const fn document(&self) -> &Document {
        &self.document
    }

    /// Returns the current epoch.
    #[must_use]
    pub const fn epoch(&self) -> Epoch {
        self.epoch
    }

    /// Takes a handle to `node` at the current epoch.
    #[must_use]
    pub const fn handle(&self, node: NodeId) -> Handle {
        Handle {
            node,
            epoch: self.epoch,
        }
    }

    /// Validates a handle against the current epoch.
    ///
    /// # Errors
    ///
    /// Returns [`DomError::StaleHandle`] if the document has mutated since the
    /// handle was taken.
    pub const fn resolve(&self, handle: Handle) -> Result<NodeId, DomError> {
        if handle.epoch.0 == self.epoch.0 {
            Ok(handle.node)
        } else {
            Err(DomError::StaleHandle {
                handle: handle.epoch,
                current: self.epoch,
            })
        }
    }

    /// Advances the epoch and records what changed.
    ///
    /// Replaces a bare `bump`, so that advancing the epoch without saying why
    /// is not expressible. The two were separate for one iteration and nothing
    /// enforced that they stayed in step; a consumer that trusts the log to
    /// explain an epoch change would have been wrong the first time they
    /// diverged, and nothing would have reported it.
    fn record(&mut self, change: Change) {
        self.epoch.0 += 1;
        self.changes.push_back(change);
        if self.changes.len() > MAX_RECORDED_CHANGES {
            self.changes.pop_front();
            self.oldest_retained.0 += 1;
        }
    }

    /// Returns the oldest epoch whose changes are still retained.
    #[must_use]
    pub const fn oldest_retained(&self) -> Epoch {
        self.oldest_retained
    }

    /// Returns the changes that have happened since `epoch`.
    ///
    /// # Errors
    ///
    /// Returns [`DomError::ChangesUnavailable`] when `epoch` is older than the
    /// retained history, or newer than the document. A caller that cannot learn
    /// what changed must treat everything as changed, which is why this refuses
    /// rather than returning the entries it still has.
    pub fn changes_since(&self, epoch: Epoch) -> Result<Vec<&Change>, DomError> {
        if epoch > self.epoch || epoch < self.oldest_retained {
            return Err(DomError::ChangesUnavailable {
                requested: epoch,
                oldest: self.oldest_retained,
                current: self.epoch,
            });
        }
        let skip = (epoch.0 - self.oldest_retained.0) as usize;
        Ok(self.changes.iter().skip(skip).collect())
    }

    // -- mutation --------------------------------------------------------

    /// Creates a detached element.
    ///
    /// # Errors
    ///
    /// Returns [`DomError::CustomElementUnsupported`] for a name containing a
    /// hyphen, which the standard reserves for custom elements whose reactions
    /// run author code during mutation.
    pub fn create_element(&mut self, name: &str) -> Result<Handle, DomError> {
        if name.contains('-') {
            return Err(DomError::CustomElementUnsupported {
                name: name.to_string(),
            });
        }
        let id = self.document.create_element(name, Vec::new());
        self.record(Change::NodeCreated { node: id });
        Ok(self.handle(id))
    }

    /// Creates a detached text node.
    pub fn create_text(&mut self, text: &str) -> Handle {
        let id = self.document.create_text(text);
        self.record(Change::NodeCreated { node: id });
        self.handle(id)
    }

    /// Appends `child` to `parent`.
    ///
    /// # Errors
    ///
    /// Returns [`DomError::StaleHandle`] if either handle predates a mutation,
    /// or a [`DomError::Mutation`] if the tree refuses the change.
    pub fn append_child(&mut self, parent: Handle, child: Handle) -> Result<(), DomError> {
        let parent = self.resolve(parent)?;
        let child = self.resolve(child)?;
        self.document.append_child(parent, child)?;
        self.record(Change::ChildList { parent });
        Ok(())
    }

    /// Inserts `child` before `reference` within `parent`.
    ///
    /// # Errors
    ///
    /// Returns [`DomError::StaleHandle`] or a [`DomError::Mutation`].
    pub fn insert_before(
        &mut self,
        parent: Handle,
        child: Handle,
        reference: Handle,
    ) -> Result<(), DomError> {
        let parent = self.resolve(parent)?;
        let child = self.resolve(child)?;
        let reference = self.resolve(reference)?;
        self.document.insert_before(parent, child, reference)?;
        self.record(Change::ChildList { parent });
        Ok(())
    }

    /// Removes `child` from its parent.
    ///
    /// # Errors
    ///
    /// Returns [`DomError::StaleHandle`] or a [`DomError::Mutation`].
    pub fn remove_child(&mut self, child: Handle) -> Result<(), DomError> {
        let child = self.resolve(child)?;
        // Read before the removal: afterwards the node has no parent, and the
        // change belongs to the list it left rather than to the node.
        let parent = self.document.node(child).parent;
        self.document.remove_child(child)?;
        if let Some(parent) = parent {
            self.record(Change::ChildList { parent });
        }
        Ok(())
    }

    /// Sets an attribute.
    ///
    /// # Errors
    ///
    /// Returns [`DomError::StaleHandle`] or a [`DomError::Mutation`].
    pub fn set_attribute(
        &mut self,
        element: Handle,
        name: &str,
        value: &str,
    ) -> Result<(), DomError> {
        let element = self.resolve(element)?;
        self.document.set_attribute(element, name, value)?;
        self.record(Change::Attribute {
            node: element,
            name: name.to_string(),
        });
        Ok(())
    }

    /// Removes an attribute.
    ///
    /// # Errors
    ///
    /// Returns [`DomError::StaleHandle`] or a [`DomError::Mutation`].
    pub fn remove_attribute(&mut self, element: Handle, name: &str) -> Result<(), DomError> {
        let element = self.resolve(element)?;
        self.document.remove_attribute(element, name)?;
        self.record(Change::Attribute {
            node: element,
            name: name.to_string(),
        });
        Ok(())
    }

    /// Attaches a shadow root.
    ///
    /// # Errors
    ///
    /// Always returns [`DomError::ShadowTreeUnsupported`]. Shadow trees
    /// retarget events, so a partial implementation would produce a wrong
    /// propagation path rather than a missing feature.
    pub const fn attach_shadow(&mut self, _host: Handle) -> Result<Handle, DomError> {
        Err(DomError::ShadowTreeUnsupported)
    }

    /// Registers a `MutationObserver`.
    ///
    /// # Errors
    ///
    /// Always returns [`DomError::MutationObserverUnsupported`], because
    /// delivery order depends on a microtask queue this crate has no scheduler
    /// for.
    pub const fn observe_mutations(&mut self, _target: Handle) -> Result<(), DomError> {
        Err(DomError::MutationObserverUnsupported)
    }

    // -- events ----------------------------------------------------------

    /// Registers a listener.
    ///
    /// `name` identifies the listener in the dispatch record. `effects`
    /// declares what it does, standing in for script until `WP-010` lands.
    ///
    /// # Errors
    ///
    /// Returns [`DomError::StaleHandle`] if the handle predates a mutation.
    pub fn add_listener(
        &mut self,
        target: Handle,
        kind: &str,
        name: &str,
        capture: bool,
        effects: &[Effect],
    ) -> Result<(), DomError> {
        let node = self.resolve(target)?;
        self.listeners.push(Listener {
            node,
            kind: kind.to_string(),
            name: name.to_string(),
            capture,
            effects: effects.to_vec(),
        });
        // Registering a listener does not change the tree, so the epoch is
        // deliberately not advanced; existing handles stay valid.
        Ok(())
    }

    /// Dispatches `event` at `target` through capture, target, and bubble.
    ///
    /// # Errors
    ///
    /// Returns [`DomError::StaleHandle`] if the handle predates a mutation.
    pub fn dispatch(&self, target: Handle, event: &Event) -> Result<Dispatch, DomError> {
        let target_node = self.resolve(target)?;
        let mut result = Dispatch::default();

        // The propagation path is root-first for capture and the reverse for
        // bubble, computed once before any listener runs so that mutations
        // during dispatch cannot reshape it.
        let mut path = self.document.ancestors(target_node);
        path.reverse();

        let mut stopped = false;

        for &node in &path {
            if stopped {
                break;
            }
            stopped = self.run_listeners(node, event, Phase::Capturing, true, &mut result);
        }

        if !stopped {
            stopped = self.run_listeners(target_node, event, Phase::AtTarget, false, &mut result);
        }

        if !stopped && event.bubbles {
            for &node in path.iter().rev() {
                if self.run_listeners(node, event, Phase::Bubbling, false, &mut result) {
                    break;
                }
            }
        }

        Ok(result)
    }

    /// Runs listeners on one node. Returns whether propagation should stop.
    fn run_listeners(
        &self,
        node: NodeId,
        event: &Event,
        phase: Phase,
        capture: bool,
        result: &mut Dispatch,
    ) -> bool {
        let mut stop_after = false;
        for listener in self.listeners.iter().filter(|listener| {
            listener.node == node
                && listener.kind == event.kind
                // At the target both capture and bubble listeners run, in
                // registration order.
                && (phase == Phase::AtTarget || listener.capture == capture)
        }) {
            result.invocations.push(Invocation {
                node,
                listener: listener.name.clone(),
                phase,
            });
            for effect in &listener.effects {
                match effect {
                    Effect::PreventDefault => {
                        if event.cancelable {
                            result.default_prevented = true;
                        }
                    }
                    Effect::StopPropagation => stop_after = true,
                    Effect::StopImmediatePropagation => return true,
                }
            }
        }
        stop_after
    }
}

/// Returns the attributes of an element, or an empty slice.
#[must_use]
pub fn attributes_of(document: &Document, node: NodeId) -> &[Attribute] {
    match &document.node(node).data {
        NodeData::Element { attributes, .. } => attributes,
        _ => &[],
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use turing_html::{Tokenizer, TreeBuilder};

    fn dom(html: &str) -> Dom {
        let tokens = Tokenizer::new(html).tokenize().expect("tokenizes").tokens;
        Dom::new(TreeBuilder::new().build(&tokens).expect("builds"))
    }

    fn find(dom: &Dom, tag: &str) -> NodeId {
        (0..dom.document().len())
            .map(NodeId::from_index)
            .find(|&id| dom.document().element_name(id) == Some(tag))
            .expect("element exists")
    }

    #[test]
    fn mutation_advances_the_epoch() {
        let mut dom = dom("<div></div>");
        let before = dom.epoch();
        let text = dom.create_text("x");
        let div = dom.handle(find(&dom, "div"));
        dom.append_child(div, text).expect("appends");
        assert!(dom.epoch() > before);
    }

    #[test]
    fn a_handle_taken_before_a_mutation_is_refused() {
        // This is the property REQ-AI-003 depends on: an agent that reads the
        // page, pauses, then acts must not address a node index that has since
        // changed meaning.
        let mut dom = dom("<div></div>");
        let stale = dom.handle(find(&dom, "div"));
        let _ = dom.create_text("forces a mutation");
        let error = dom.resolve(stale).expect_err("stale handle refused");
        assert!(matches!(error, DomError::StaleHandle { .. }));
    }

    #[test]
    fn a_handle_taken_after_a_mutation_is_accepted() {
        let mut dom = dom("<div></div>");
        let _ = dom.create_text("x");
        let fresh = dom.handle(find(&dom, "div"));
        assert!(dom.resolve(fresh).is_ok());
    }

    #[test]
    fn registering_a_listener_does_not_invalidate_handles() {
        // Listener registration is not a structural change, so bumping the
        // epoch here would make normal event wiring impossible.
        let mut dom = dom("<div></div>");
        let div = dom.handle(find(&dom, "div"));
        dom.add_listener(div, "click", "a", false, &[])
            .expect("registers");
        assert!(dom.resolve(div).is_ok());
    }

    #[test]
    fn append_moves_a_node_between_parents() {
        let mut dom = dom("<div id=\"a\"></div><section></section>");
        let text = dom.create_text("x");
        let div = dom.handle(find(&dom, "div"));
        dom.append_child(div, text).expect("appends");

        let section = dom.handle(find(&dom, "section"));
        let text = dom.handle(text.node());
        dom.append_child(section, text).expect("moves");

        let div_id = find(&dom, "div");
        let section_id = find(&dom, "section");
        assert!(dom.document().node(div_id).children.is_empty());
        assert_eq!(dom.document().node(section_id).children.len(), 1);
    }

    #[test]
    fn insert_before_places_a_node_at_the_right_index() {
        let mut dom = dom("<ul><li>a</li><li>b</li></ul>");
        let list = dom.handle(find(&dom, "ul"));
        let inserted = dom.create_element("li").expect("creates");
        let list = dom.handle(list.node());
        let first = dom.document().node(list.node()).children[0];
        let first = dom.handle(first);
        dom.insert_before(list, inserted, first).expect("inserts");
        assert_eq!(
            dom.document().node(list.node()).children[0],
            inserted.node()
        );
    }

    #[test]
    fn removal_detaches_the_node() {
        let mut dom = dom("<div><span>x</span></div>");
        let span = dom.handle(find(&dom, "span"));
        dom.remove_child(span).expect("removes");
        let div = find(&dom, "div");
        assert!(dom.document().node(div).children.is_empty());
    }

    #[test]
    fn attributes_can_be_set_and_removed() {
        let mut dom = dom("<div></div>");
        let div = dom.handle(find(&dom, "div"));
        dom.set_attribute(div, "class", "x").expect("sets");
        let div = dom.handle(div.node());
        assert_eq!(attributes_of(dom.document(), div.node())[0].value, "x");
        dom.remove_attribute(div, "class").expect("removes");
        assert!(attributes_of(dom.document(), div.node()).is_empty());
    }

    #[test]
    fn a_node_cannot_become_its_own_ancestor() {
        // A cycle would make traversal non-terminating, so it is refused.
        let mut dom = dom("<div><span></span></div>");
        let div = dom.handle(find(&dom, "div"));
        let span = dom.handle(find(&dom, "span"));
        let error = dom.append_child(span, div).expect_err("cycle refused");
        assert!(matches!(
            error,
            DomError::Mutation(MutationError::HierarchyRequest)
        ));
    }

    #[test]
    fn dispatch_runs_capture_then_target_then_bubble() {
        let mut dom = dom("<div><section><p>x</p></section></div>");
        let div = dom.handle(find(&dom, "div"));
        dom.add_listener(div, "click", "div-capture", true, &[])
            .expect("registers");
        dom.add_listener(div, "click", "div-bubble", false, &[])
            .expect("registers");
        let paragraph = dom.handle(find(&dom, "p"));
        dom.add_listener(paragraph, "click", "p-target", false, &[])
            .expect("registers");

        let result = dom
            .dispatch(paragraph, &Event::new("click"))
            .expect("dispatches");
        let order: Vec<_> = result
            .invocations
            .iter()
            .map(|i| (i.listener.as_str(), i.phase))
            .collect();
        assert_eq!(
            order,
            vec![
                ("div-capture", Phase::Capturing),
                ("p-target", Phase::AtTarget),
                ("div-bubble", Phase::Bubbling),
            ]
        );
    }

    #[test]
    fn non_bubbling_events_do_not_run_bubble_listeners() {
        let mut dom = dom("<div><p>x</p></div>");
        let div = dom.handle(find(&dom, "div"));
        dom.add_listener(div, "focus", "div-bubble", false, &[])
            .expect("registers");
        let paragraph = dom.handle(find(&dom, "p"));
        let result = dom
            .dispatch(paragraph, &Event::non_bubbling("focus"))
            .expect("dispatches");
        assert!(result.invocations.is_empty());
    }

    #[test]
    fn stop_propagation_halts_after_the_current_node() {
        let mut dom = dom("<div><section><p>x</p></section></div>");
        let section = dom.handle(find(&dom, "section"));
        dom.add_listener(
            section,
            "click",
            "section-capture",
            true,
            &[Effect::StopPropagation],
        )
        .expect("registers");
        let paragraph = dom.handle(find(&dom, "p"));
        dom.add_listener(paragraph, "click", "p-target", false, &[])
            .expect("registers");

        let result = dom
            .dispatch(paragraph, &Event::new("click"))
            .expect("dispatches");
        // The target listener must not run once capture stopped propagation.
        assert_eq!(result.invocations.len(), 1);
        assert_eq!(result.invocations[0].listener, "section-capture");
    }

    #[test]
    fn stop_immediate_propagation_skips_later_listeners_on_the_same_node() {
        let mut dom = dom("<div><p>x</p></div>");
        let paragraph = dom.handle(find(&dom, "p"));
        dom.add_listener(
            paragraph,
            "click",
            "first",
            false,
            &[Effect::StopImmediatePropagation],
        )
        .expect("registers");
        dom.add_listener(paragraph, "click", "second", false, &[])
            .expect("registers");

        let result = dom
            .dispatch(paragraph, &Event::new("click"))
            .expect("dispatches");
        assert_eq!(result.invocations.len(), 1);
        assert_eq!(result.invocations[0].listener, "first");
    }

    #[test]
    fn prevent_default_is_recorded() {
        let mut dom = dom("<div><a>x</a></div>");
        let anchor = dom.handle(find(&dom, "a"));
        dom.add_listener(anchor, "click", "block", false, &[Effect::PreventDefault])
            .expect("registers");
        let result = dom
            .dispatch(anchor, &Event::new("click"))
            .expect("dispatches");
        assert!(result.default_prevented);
    }

    #[test]
    fn prevent_default_is_ignored_on_a_non_cancelable_event() {
        let mut dom = dom("<div><a>x</a></div>");
        let anchor = dom.handle(find(&dom, "a"));
        dom.add_listener(anchor, "click", "block", false, &[Effect::PreventDefault])
            .expect("registers");
        let event = Event {
            kind: "click".to_string(),
            bubbles: true,
            cancelable: false,
        };
        let result = dom.dispatch(anchor, &event).expect("dispatches");
        assert!(!result.default_prevented);
    }

    #[test]
    fn listeners_for_other_event_types_do_not_run() {
        let mut dom = dom("<div><p>x</p></div>");
        let paragraph = dom.handle(find(&dom, "p"));
        dom.add_listener(paragraph, "keydown", "other", false, &[])
            .expect("registers");
        let result = dom
            .dispatch(paragraph, &Event::new("click"))
            .expect("dispatches");
        assert!(result.invocations.is_empty());
    }

    #[test]
    fn shadow_trees_are_reported_not_guessed() {
        let mut dom = dom("<div></div>");
        let div = dom.handle(find(&dom, "div"));
        let error = dom.attach_shadow(div).expect_err("refused");
        assert!(matches!(error, DomError::ShadowTreeUnsupported));
    }

    #[test]
    fn custom_elements_are_reported_not_guessed() {
        let mut dom = dom("<div></div>");
        let error = dom.create_element("my-widget").expect_err("refused");
        assert!(matches!(error, DomError::CustomElementUnsupported { .. }));
    }

    #[test]
    fn mutation_observers_are_reported_not_guessed() {
        let mut dom = dom("<div></div>");
        let div = dom.handle(find(&dom, "div"));
        let error = dom.observe_mutations(div).expect_err("refused");
        assert!(matches!(error, DomError::MutationObserverUnsupported));
    }

    #[test]
    fn mutating_during_a_session_invalidates_earlier_handles_end_to_end() {
        let mut dom = dom("<div><p>x</p></div>");
        let paragraph = dom.handle(find(&dom, "p"));
        dom.add_listener(paragraph, "click", "target", false, &[])
            .expect("registers");
        // A mutation between reading and acting must invalidate the handle.
        let _ = dom.create_text("mutation");
        let error = dom
            .dispatch(paragraph, &Event::new("click"))
            .expect_err("stale dispatch refused");
        assert!(matches!(error, DomError::StaleHandle { .. }));
    }
    #[test]
    fn a_refused_mutation_does_not_advance_the_epoch() {
        // The epoch is what tells every consumer of this document that cached
        // work is stale. Advancing it for a mutation that did not happen would
        // let a script full of invalid calls invalidate every cached layout
        // while changing nothing.
        //
        // A text node is the reachable case: it has a valid handle and cannot
        // carry attributes, so the refusal happens inside the mutation rather
        // than at handle resolution. Reaching that path is the whole point — an
        // equivalent test written against a missing element stops earlier and
        // proves nothing about the ordering here.
        let mut dom = dom("<html><body><p>x</p></body></html>");
        let text = dom.create_text("loose");
        let settled = dom.epoch();

        assert!(dom.set_attribute(text, "class", "x").is_err());
        assert_eq!(dom.epoch(), settled, "a refused set must not advance it");

        assert!(dom.remove_attribute(text, "class").is_err());
        assert_eq!(dom.epoch(), settled, "a refused removal must not either");
    }

    #[test]
    fn a_successful_mutation_does_advance_the_epoch() {
        // The other side. An epoch that never moved would pass the test above
        // and tell every consumer that nothing ever changes.
        let mut dom = dom("<html><body><p id='a'>x</p></body></html>");
        let node = dom
            .document()
            .element_by_id("a")
            .expect("the element exists");
        let handle = dom.handle(node);
        let before = dom.epoch();

        dom.set_attribute(handle, "class", "x").expect("sets");
        assert!(dom.epoch() > before);
    }
    // -- the change log --------------------------------------------------

    #[test]
    fn every_epoch_advance_has_a_recorded_change() {
        // The invariant the whole log rests on. A consumer asks "what changed
        // since epoch N" precisely because the epoch moved; if the two can
        // diverge, the answer is wrong in a way the caller cannot detect.
        //
        // Structural rather than conventional — `record` is the only way to
        // advance the epoch — but asserted because the structure is easy to
        // undo and nothing else would notice.
        let mut dom = dom("<html><body><p id='a'>x</p></body></html>");
        let start = dom.epoch();

        let node = dom.document().element_by_id("a").expect("exists");
        // Re-minted each time: every mutation advances the epoch, which makes
        // every outstanding handle stale. Conservative and deliberate — a
        // handle taken before a change cannot be assumed to still mean what it
        // did — but it means a caller performing several mutations re-acquires
        // between them.
        let handle = dom.handle(node);
        dom.set_attribute(handle, "class", "one").expect("sets");
        let handle = dom.handle(node);
        dom.set_attribute(handle, "class", "two").expect("sets");
        let handle = dom.handle(node);
        dom.remove_attribute(handle, "class").expect("removes");

        let advanced = dom.epoch().value() - start.value();
        let recorded = dom.changes_since(start).expect("available").len();
        assert_eq!(advanced, 3);
        assert_eq!(recorded as u64, advanced, "one change per advance");
    }

    #[test]
    fn a_refused_mutation_records_nothing() {
        // Follows from recording after the fallible step, and worth pinning
        // separately: a log entry for a change that did not happen would send a
        // consumer looking for a difference that is not there.
        let mut dom = dom("<html><body><p>x</p></body></html>");
        let text = dom.create_text("loose");
        let settled = dom.epoch();

        assert!(dom.set_attribute(text, "class", "x").is_err());

        assert!(dom.changes_since(settled).expect("available").is_empty());
        assert_eq!(dom.epoch(), settled);
    }

    #[test]
    fn a_change_names_the_node_and_what_changed() {
        let mut dom = dom("<html><body><p id='a'>x</p></body></html>");
        let node = dom.document().element_by_id("a").expect("exists");
        let handle = dom.handle(node);
        let before = dom.epoch();

        dom.set_attribute(handle, "data-role", "panel")
            .expect("sets");

        let changes = dom.changes_since(before).expect("available");
        assert_eq!(
            changes,
            vec![&Change::Attribute {
                node,
                name: "data-role".to_string()
            }]
        );
    }

    #[test]
    fn removing_a_child_records_the_list_it_left() {
        // The parent has to be read before the removal: afterwards the node has
        // none, and a change recorded against the detached node would tell a
        // consumer nothing about which subtree to re-examine.
        let mut dom = dom("<html><body><p id='a'>x</p></body></html>");
        let node = dom.document().element_by_id("a").expect("exists");
        let parent = dom.document().node(node).parent.expect("has a parent");
        let handle = dom.handle(node);
        let before = dom.epoch();

        dom.remove_child(handle).expect("removes");

        assert_eq!(
            dom.changes_since(before).expect("available"),
            vec![&Change::ChildList { parent }]
        );
    }

    #[test]
    fn a_query_from_the_current_epoch_is_empty_rather_than_an_error() {
        // Nothing has changed since now. An error here would make every caller
        // treat a quiet document as an unknown one.
        let dom = dom("<html><body><p>x</p></body></html>");
        assert!(
            dom.changes_since(dom.epoch())
                .expect("available")
                .is_empty()
        );
    }

    #[test]
    fn a_query_from_the_future_is_refused() {
        let dom = dom("<html><body><p>x</p></body></html>");
        assert!(matches!(
            dom.changes_since(Epoch::from_value(dom.epoch().value() + 1)),
            Err(DomError::ChangesUnavailable { .. })
        ));
    }

    #[test]
    fn a_query_older_than_the_retained_history_is_refused() {
        // Not answered with what remains. A partial answer understates what
        // changed and a consumer would act on it as though it were complete,
        // which is worse than being told to assume everything changed.
        let mut dom = dom("<html><body><p id='a'>x</p></body></html>");
        let node = dom.document().element_by_id("a").expect("exists");
        let start = dom.epoch();

        for i in 0..MAX_RECORDED_CHANGES + 10 {
            let handle = dom.handle(node);
            dom.set_attribute(handle, "class", &format!("v{i}"))
                .expect("sets");
        }

        assert!(matches!(
            dom.changes_since(start),
            Err(DomError::ChangesUnavailable { .. })
        ));
        // Recent history is still answerable.
        let recent = Epoch::from_value(dom.epoch().value() - 5);
        assert_eq!(dom.changes_since(recent).expect("available").len(), 5);
    }

    #[test]
    fn the_log_does_not_grow_without_bound() {
        // A script mutates in a loop, so this is attacker-influenced and
        // bounded like every other growth path here.
        let mut dom = dom("<html><body><p id='a'>x</p></body></html>");
        let node = dom.document().element_by_id("a").expect("exists");
        for i in 0..MAX_RECORDED_CHANGES * 3 {
            let handle = dom.handle(node);
            dom.set_attribute(handle, "class", &format!("v{i}"))
                .expect("sets");
        }

        let all = dom.changes_since(dom.oldest_retained()).expect("available");
        assert_eq!(all.len(), MAX_RECORDED_CHANGES);
    }

    #[test]
    fn registering_a_listener_records_nothing() {
        // Listener registration does not advance the epoch, so it must not
        // appear in the log either — the two have to agree about what counts as
        // a change, or a consumer reconciling them finds a discrepancy that is
        // not real.
        let mut dom = dom("<html><body><p id='a'>x</p></body></html>");
        let node = dom.document().element_by_id("a").expect("exists");
        let handle = dom.handle(node);
        let before = dom.epoch();

        dom.add_listener(handle, "click", "handler", false, &[])
            .expect("registers");

        assert_eq!(dom.epoch(), before);
        assert!(dom.changes_since(before).expect("available").is_empty());
    }
}
