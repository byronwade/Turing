// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Turing-owned exact tracing garbage collector and Web IDL binding registry.
//!
//! This crate implements `WP-011`, `REQ-JS-002`, and `REQ-JS-003`: a
//! mark-and-sweep heap that traces precisely, and the registry that will bind
//! script-visible interfaces to engine operations. It derives from no existing
//! engine, consistent with `ADR-0009` Option A.
//!
//! # Why exact rather than conservative
//!
//! A conservative collector scans memory it does not understand and treats any
//! bit pattern resembling a pointer as one. That is easier to retrofit, but it
//! retains garbage unpredictably and, in a browser, gives a page a way to
//! influence what stays alive. This heap is exact: every object declares its
//! outgoing references through [`Trace`], so reachability is computed from
//! structure rather than guessed from memory.
//!
//! # Why handles carry a generation
//!
//! A slot freed by collection is reused. A bare index into the heap would then
//! silently address a different object, which is the memory-safety bug class
//! this engine exists to avoid, reintroduced at a higher level. Every slot
//! carries a generation counter, and [`GcRef`] records the generation it was
//! taken at, so a reference to a collected object is refused rather than
//! quietly resolved. This is the same discipline `turing-dom` applies with
//! document epochs, for the same reason.
//!
//! # Deliberate limits
//!
//! Implemented: allocation, exact tracing through object graphs, root sets,
//! mark-and-sweep collection, cycle reclamation, generation-checked handles,
//! and heap statistics.
//!
//! Not implemented, each returning a typed error rather than an approximation:
//!
//! - generational and incremental collection, which change pause behaviour and
//!   need write barriers this heap does not have;
//! - weak references and finalizers, whose observable timing is specified and
//!   would otherwise be invented;
//! - cross-heap references, which a multi-process engine needs and which
//!   cannot be traced from inside one heap.

#![forbid(unsafe_code)]

use core::fmt;
use std::collections::BTreeMap;

/// A reference to a heap object, valid only for the generation it was taken at.
#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct GcRef {
    index: usize,
    generation: u32,
}

impl GcRef {
    /// Returns the slot index, without checking that it is still live.
    #[must_use]
    pub const fn index(self) -> usize {
        self.index
    }

    /// Returns the generation this reference was taken at.
    #[must_use]
    pub const fn generation(self) -> u32 {
        self.generation
    }
}

impl fmt::Display for GcRef {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(formatter, "gc[{}#{}]", self.index, self.generation)
    }
}

/// A heap operation that was refused.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum GcError {
    /// The reference names a slot that has since been collected and reused.
    DanglingReference { reference: GcRef, current: u32 },
    /// Generational and incremental collection need write barriers.
    IncrementalCollectionUnsupported,
    /// Weak reference and finalizer timing is observable and specified.
    WeakReferenceUnsupported,
    /// A reference into another heap cannot be traced from this one.
    CrossHeapReferenceUnsupported,
    /// The interface or operation is not bound.
    UnboundOperation {
        interface: String,
        operation: String,
    },
}

impl fmt::Display for GcError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::DanglingReference { reference, current } => write!(
                formatter,
                "refused: {reference} names a slot now at generation {current}"
            ),
            Self::IncrementalCollectionUnsupported => write!(
                formatter,
                "incremental and generational collection are not implemented; they require write barriers"
            ),
            Self::WeakReferenceUnsupported => write!(
                formatter,
                "weak references and finalizers are not implemented; their timing is observable and specified"
            ),
            Self::CrossHeapReferenceUnsupported => write!(
                formatter,
                "cross-heap references are not implemented; they cannot be traced from inside one heap"
            ),
            Self::UnboundOperation {
                interface,
                operation,
            } => write!(formatter, "{interface}.{operation} is not bound"),
        }
    }
}

/// An object's payload.
///
/// The collector does not interpret these beyond tracing; the shapes exist so
/// the heap can hold what a script-visible object graph actually contains.
#[derive(Clone, Debug, PartialEq)]
pub enum Payload {
    /// A plain value with no outgoing references.
    Value(String),
    /// A property bag. Property order is stable so traversal is deterministic,
    /// which matters when comparing collection behaviour across runs.
    Object(BTreeMap<String, GcRef>),
    /// A binding to a host object, identified by interface and node index.
    HostObject { interface: String, node: usize },
    /// A closure capturing an environment.
    Closure {
        function: usize,
        captured: Vec<GcRef>,
    },
}

/// Declares an object's outgoing references.
///
/// Exactness lives here: the collector never guesses which words are pointers,
/// it asks.
pub trait Trace {
    /// Appends every reference this value holds to `out`.
    fn trace(&self, out: &mut Vec<GcRef>);
}

impl Trace for Payload {
    fn trace(&self, out: &mut Vec<GcRef>) {
        match self {
            Self::Value(_) | Self::HostObject { .. } => {}
            Self::Object(properties) => out.extend(properties.values().copied()),
            Self::Closure { captured, .. } => out.extend(captured.iter().copied()),
        }
    }
}

#[derive(Clone, Debug)]
struct Slot {
    payload: Option<Payload>,
    generation: u32,
    marked: bool,
}

/// Counts describing a collection.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub struct Statistics {
    /// Objects live after the most recent collection.
    pub live: usize,
    /// Objects reclaimed by the most recent collection.
    pub collected: usize,
    /// Collections performed.
    pub collections: u64,
}

/// A mark-and-sweep heap.
#[derive(Debug, Default)]
pub struct Heap {
    slots: Vec<Slot>,
    free: Vec<usize>,
    roots: Vec<GcRef>,
    statistics: Statistics,
}

impl Heap {
    /// Creates an empty heap.
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    /// Allocates `payload` and returns a reference to it.
    pub fn allocate(&mut self, payload: Payload) -> GcRef {
        // Reusing a freed slot bumps its generation, which is what makes an
        // older reference to that slot detectable rather than silently valid.
        if let Some(index) = self.free.pop() {
            let slot = &mut self.slots[index];
            slot.payload = Some(payload);
            slot.marked = false;
            return GcRef {
                index,
                generation: slot.generation,
            };
        }
        let index = self.slots.len();
        self.slots.push(Slot {
            payload: Some(payload),
            generation: 0,
            marked: false,
        });
        GcRef {
            index,
            generation: 0,
        }
    }

    /// Returns whether `reference` still names a live object.
    #[must_use]
    pub fn is_live(&self, reference: GcRef) -> bool {
        self.slots
            .get(reference.index)
            .is_some_and(|slot| slot.generation == reference.generation && slot.payload.is_some())
    }

    /// Reads an object.
    ///
    /// # Errors
    ///
    /// Returns [`GcError::DanglingReference`] if the slot has been collected
    /// and reused, rather than returning whatever now occupies it.
    pub fn get(&self, reference: GcRef) -> Result<&Payload, GcError> {
        let slot = self
            .slots
            .get(reference.index)
            .ok_or(GcError::DanglingReference {
                reference,
                current: 0,
            })?;
        if slot.generation != reference.generation {
            return Err(GcError::DanglingReference {
                reference,
                current: slot.generation,
            });
        }
        slot.payload.as_ref().ok_or(GcError::DanglingReference {
            reference,
            current: slot.generation,
        })
    }

    /// Replaces an object's payload.
    ///
    /// # Errors
    ///
    /// Returns [`GcError::DanglingReference`] for a stale reference.
    pub fn set(&mut self, reference: GcRef, payload: Payload) -> Result<(), GcError> {
        let current = self
            .slots
            .get(reference.index)
            .map_or(0, |slot| slot.generation);
        if !self.is_live(reference) {
            return Err(GcError::DanglingReference { reference, current });
        }
        self.slots[reference.index].payload = Some(payload);
        Ok(())
    }

    /// Adds a root. Roots and everything reachable from them survive.
    pub fn add_root(&mut self, reference: GcRef) {
        if !self.roots.contains(&reference) {
            self.roots.push(reference);
        }
    }

    /// Removes a root.
    pub fn remove_root(&mut self, reference: GcRef) {
        self.roots.retain(|&existing| existing != reference);
    }

    /// Returns the current statistics.
    #[must_use]
    pub const fn statistics(&self) -> Statistics {
        self.statistics
    }

    /// Returns the number of live objects.
    #[must_use]
    pub fn live_count(&self) -> usize {
        self.slots.iter().filter(|s| s.payload.is_some()).count()
    }

    /// Runs a full mark-and-sweep collection and returns the number reclaimed.
    ///
    /// Tracing is exact and iterative. An explicit worklist rather than
    /// recursion keeps a deeply nested object graph from exhausting the native
    /// stack, which a hostile page could otherwise arrange.
    pub fn collect(&mut self) -> usize {
        for slot in &mut self.slots {
            slot.marked = false;
        }

        let mut worklist: Vec<GcRef> = self
            .roots
            .iter()
            .copied()
            .filter(|&reference| self.is_live(reference))
            .collect();

        let mut outgoing = Vec::new();
        while let Some(reference) = worklist.pop() {
            let Some(slot) = self.slots.get_mut(reference.index) else {
                continue;
            };
            if slot.generation != reference.generation || slot.payload.is_none() {
                continue;
            }
            if slot.marked {
                // Already visited. This is what makes cycles terminate.
                continue;
            }
            slot.marked = true;
            outgoing.clear();
            if let Some(payload) = &slot.payload {
                payload.trace(&mut outgoing);
            }
            worklist.extend(outgoing.iter().copied());
        }

        let mut collected = 0;
        for index in 0..self.slots.len() {
            let slot = &mut self.slots[index];
            if slot.payload.is_some() && !slot.marked {
                slot.payload = None;
                slot.generation = slot.generation.wrapping_add(1);
                self.free.push(index);
                collected += 1;
            }
        }

        self.statistics.collections += 1;
        self.statistics.collected = collected;
        self.statistics.live = self.live_count();
        collected
    }

    /// Requests incremental collection.
    ///
    /// # Errors
    ///
    /// Always returns [`GcError::IncrementalCollectionUnsupported`]. Pause
    /// behaviour is a user-visible property, so an implementation that claimed
    /// to be incremental while stopping the world would misreport it.
    pub const fn collect_incremental(&mut self) -> Result<usize, GcError> {
        Err(GcError::IncrementalCollectionUnsupported)
    }

    /// Allocates a weak reference.
    ///
    /// # Errors
    ///
    /// Always returns [`GcError::WeakReferenceUnsupported`], because when a
    /// weak reference clears and when a finalizer runs are specified and
    /// observable.
    pub const fn allocate_weak(&mut self, _target: GcRef) -> Result<GcRef, GcError> {
        Err(GcError::WeakReferenceUnsupported)
    }

    /// Records a reference into another heap.
    ///
    /// # Errors
    ///
    /// Always returns [`GcError::CrossHeapReferenceUnsupported`]. A reference
    /// this heap cannot trace would be either wrongly collected or wrongly
    /// retained.
    pub const fn add_cross_heap_reference(&mut self, _target: usize) -> Result<(), GcError> {
        Err(GcError::CrossHeapReferenceUnsupported)
    }
}

// -- Web IDL bindings ----------------------------------------------------

/// An operation exposed to script by a host interface.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Operation {
    /// Interface name, such as `Node`.
    pub interface: String,
    /// Operation name, such as `appendChild`.
    pub name: String,
    /// Declared argument count.
    pub arity: usize,
}

/// The set of interfaces and operations script may reach.
///
/// A registry rather than direct calls, because the security model requires
/// that the reachable surface be enumerable. `REQ-AI-001` treats agents as
/// separately identified principals, and a capability that cannot be listed
/// cannot be granted or revoked.
#[derive(Debug, Default)]
pub struct Bindings {
    operations: Vec<Operation>,
}

impl Bindings {
    /// Creates an empty registry.
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    /// Registers an operation.
    pub fn register(&mut self, interface: &str, name: &str, arity: usize) {
        self.operations.push(Operation {
            interface: interface.to_string(),
            name: name.to_string(),
            arity,
        });
    }

    /// Returns every registered operation, so the surface can be audited.
    #[must_use]
    pub fn operations(&self) -> &[Operation] {
        &self.operations
    }

    /// Looks up an operation.
    ///
    /// # Errors
    ///
    /// Returns [`GcError::UnboundOperation`] when the interface or operation is
    /// not registered, rather than treating an unknown name as a no-op.
    pub fn resolve(&self, interface: &str, name: &str) -> Result<&Operation, GcError> {
        self.operations
            .iter()
            .find(|operation| operation.interface == interface && operation.name == name)
            .ok_or_else(|| GcError::UnboundOperation {
                interface: interface.to_string(),
                operation: name.to_string(),
            })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn value(text: &str) -> Payload {
        Payload::Value(text.to_string())
    }

    fn object(pairs: &[(&str, GcRef)]) -> Payload {
        Payload::Object(
            pairs
                .iter()
                .map(|(key, reference)| ((*key).to_string(), *reference))
                .collect(),
        )
    }

    #[test]
    fn allocation_returns_a_live_reference() {
        let mut heap = Heap::new();
        let reference = heap.allocate(value("a"));
        assert!(heap.is_live(reference));
        assert_eq!(heap.get(reference).expect("reads"), &value("a"));
    }

    #[test]
    fn unreachable_objects_are_collected() {
        let mut heap = Heap::new();
        let _garbage = heap.allocate(value("garbage"));
        assert_eq!(heap.live_count(), 1);
        assert_eq!(heap.collect(), 1);
        assert_eq!(heap.live_count(), 0);
    }

    #[test]
    fn rooted_objects_survive() {
        let mut heap = Heap::new();
        let kept = heap.allocate(value("kept"));
        heap.add_root(kept);
        let _dropped = heap.allocate(value("dropped"));
        assert_eq!(heap.collect(), 1);
        assert!(heap.is_live(kept));
    }

    #[test]
    fn objects_reachable_from_a_root_survive() {
        let mut heap = Heap::new();
        let leaf = heap.allocate(value("leaf"));
        let root = heap.allocate(object(&[("child", leaf)]));
        heap.add_root(root);
        assert_eq!(heap.collect(), 0);
        assert!(heap.is_live(leaf));
    }

    #[test]
    fn dropping_a_root_makes_its_graph_collectable() {
        let mut heap = Heap::new();
        let leaf = heap.allocate(value("leaf"));
        let root = heap.allocate(object(&[("child", leaf)]));
        heap.add_root(root);
        heap.collect();
        heap.remove_root(root);
        // Both the root object and its child become unreachable.
        assert_eq!(heap.collect(), 2);
    }

    #[test]
    fn reference_cycles_are_collected() {
        // This is the property that separates a tracing collector from
        // reference counting. Two objects pointing at each other with nothing
        // else referring to them are garbage.
        let mut heap = Heap::new();
        let first = heap.allocate(value("first"));
        let second = heap.allocate(object(&[("peer", first)]));
        heap.set(first, object(&[("peer", second)])).expect("sets");
        assert_eq!(heap.live_count(), 2);
        assert_eq!(heap.collect(), 2);
        assert_eq!(heap.live_count(), 0);
    }

    #[test]
    fn a_rooted_cycle_survives() {
        let mut heap = Heap::new();
        let first = heap.allocate(value("first"));
        let second = heap.allocate(object(&[("peer", first)]));
        heap.set(first, object(&[("peer", second)])).expect("sets");
        heap.add_root(first);
        assert_eq!(heap.collect(), 0);
        assert!(heap.is_live(first) && heap.is_live(second));
    }

    #[test]
    fn a_reference_to_a_collected_object_is_refused() {
        // The slot is reused, so a bare index would silently resolve to a
        // different object. The generation check is what prevents that.
        let mut heap = Heap::new();
        let stale = heap.allocate(value("old"));
        heap.collect();
        let fresh = heap.allocate(value("new"));
        assert_eq!(stale.index(), fresh.index(), "slot was not reused");
        let error = heap.get(stale).expect_err("stale reference refused");
        assert!(matches!(error, GcError::DanglingReference { .. }));
        assert_eq!(heap.get(fresh).expect("reads"), &value("new"));
    }

    #[test]
    fn writing_through_a_stale_reference_is_refused() {
        let mut heap = Heap::new();
        let stale = heap.allocate(value("old"));
        heap.collect();
        let error = heap.set(stale, value("x")).expect_err("refused");
        assert!(matches!(error, GcError::DanglingReference { .. }));
    }

    #[test]
    fn closures_keep_their_captures_alive() {
        let mut heap = Heap::new();
        let captured = heap.allocate(value("captured"));
        let closure = heap.allocate(Payload::Closure {
            function: 0,
            captured: vec![captured],
        });
        heap.add_root(closure);
        assert_eq!(heap.collect(), 0);
        assert!(heap.is_live(captured));
    }

    #[test]
    fn host_objects_hold_no_traced_references() {
        // A host object names a DOM node by index; the node's lifetime belongs
        // to the document, not this heap.
        let mut heap = Heap::new();
        let host = heap.allocate(Payload::HostObject {
            interface: "Node".to_string(),
            node: 7,
        });
        heap.add_root(host);
        let mut out = Vec::new();
        heap.get(host).expect("reads").trace(&mut out);
        assert!(out.is_empty());
    }

    #[test]
    fn deep_graphs_do_not_exhaust_the_stack() {
        // A hostile page could nest objects arbitrarily; tracing must be
        // iterative rather than recursive.
        let mut heap = Heap::new();
        let mut previous = heap.allocate(value("leaf"));
        for _ in 0..50_000 {
            previous = heap.allocate(object(&[("next", previous)]));
        }
        heap.add_root(previous);
        assert_eq!(heap.collect(), 0);
        assert_eq!(heap.live_count(), 50_001);
    }

    #[test]
    fn statistics_track_collections() {
        let mut heap = Heap::new();
        let kept = heap.allocate(value("kept"));
        heap.add_root(kept);
        let _garbage = heap.allocate(value("garbage"));
        heap.collect();
        let statistics = heap.statistics();
        assert_eq!(statistics.collections, 1);
        assert_eq!(statistics.collected, 1);
        assert_eq!(statistics.live, 1);
    }

    #[test]
    fn collecting_twice_reclaims_nothing_new() {
        let mut heap = Heap::new();
        let _garbage = heap.allocate(value("garbage"));
        assert_eq!(heap.collect(), 1);
        assert_eq!(heap.collect(), 0);
    }

    #[test]
    fn incremental_collection_is_refused_not_faked() {
        let mut heap = Heap::new();
        let error = heap.collect_incremental().expect_err("refused");
        assert!(matches!(error, GcError::IncrementalCollectionUnsupported));
    }

    #[test]
    fn weak_references_are_refused_not_faked() {
        let mut heap = Heap::new();
        let target = heap.allocate(value("t"));
        let error = heap.allocate_weak(target).expect_err("refused");
        assert!(matches!(error, GcError::WeakReferenceUnsupported));
    }

    #[test]
    fn cross_heap_references_are_refused() {
        let mut heap = Heap::new();
        let error = heap.add_cross_heap_reference(3).expect_err("refused");
        assert!(matches!(error, GcError::CrossHeapReferenceUnsupported));
    }

    #[test]
    fn bindings_resolve_registered_operations() {
        let mut bindings = Bindings::new();
        bindings.register("Node", "appendChild", 1);
        let operation = bindings.resolve("Node", "appendChild").expect("resolves");
        assert_eq!(operation.arity, 1);
    }

    #[test]
    fn unbound_operations_are_refused_not_treated_as_no_ops() {
        let bindings = Bindings::new();
        let error = bindings
            .resolve("Node", "removeChild")
            .expect_err("refused");
        assert!(matches!(error, GcError::UnboundOperation { .. }));
    }

    #[test]
    fn the_bound_surface_is_enumerable() {
        // A capability that cannot be listed cannot be granted or revoked,
        // which REQ-AI-001 requires of an agent principal.
        let mut bindings = Bindings::new();
        bindings.register("Node", "appendChild", 1);
        bindings.register("Element", "setAttribute", 2);
        assert_eq!(bindings.operations().len(), 2);
    }
}
