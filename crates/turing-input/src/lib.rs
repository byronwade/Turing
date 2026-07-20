// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Turing-owned routing from a pointer location to a DOM event target.
//!
//! The blueprint describes input as normalized by the platform adapter and then
//! "routed through hit testing to event targets". Hit testing answers which node
//! is at a point, and the DOM dispatches events to a target; this is the join
//! between them, completing the input half of `WP-007` alongside `REQ-ENG-005`.
//!
//! # Why this is its own crate
//!
//! Layering. `turing-dom` must not depend on `turing-layout`: a document's
//! structure and its geometry are separate concerns, and a DOM that imported
//! layout would make every consumer of the DOM carry a layout engine. Routing
//! needs both, so it sits above both rather than pushing the dependency into
//! either.
//!
//! # The hazard this exists to make visible
//!
//! A layout box tree is a photograph of the DOM at one moment. Hit testing it
//! yields a node index that was correct when layout ran. If the DOM has changed
//! since — a node removed, a subtree replaced — that index may name a different
//! node, or one no longer attached, and dispatching to it delivers the event to
//! the wrong target.
//!
//! Nothing about that failure is visible in a test where the document does not
//! change between layout and click, which is every obvious test. So the epoch
//! the layout was computed at is captured up front and checked at dispatch, and
//! a mismatch is refused.
//!
//! Minting the handle at dispatch time would defeat this entirely:
//! [`turing_dom::Dom::handle`] stamps the *current* epoch, so a handle made then
//! is valid by construction no matter how stale the hit that produced it. The
//! check has to compare against the epoch layout was computed at, which is why
//! [`HitRouter`] holds one.

#![forbid(unsafe_code)]

use core::fmt;
use turing_dom::{Dispatch, Dom, DomError, Epoch, Event};
use turing_html::NodeId;
use turing_layout::{LayoutBox, Point, hit_test};

/// A reason routing refused to deliver an event.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum InputError {
    /// The document changed after the layout being hit-tested was computed.
    LayoutOutOfDate { computed_at: Epoch, current: Epoch },
    /// The DOM refused the dispatch.
    Dispatch(DomError),
}

impl fmt::Display for InputError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::LayoutOutOfDate {
                computed_at,
                current,
            } => write!(
                formatter,
                "the layout was computed at epoch {} and the document is now at \
                 epoch {}; a hit against stale geometry names whichever node used \
                 to be there, so delivering it would dispatch to the wrong target",
                computed_at.value(),
                current.value()
            ),
            Self::Dispatch(error) => write!(formatter, "{error}"),
        }
    }
}

impl From<DomError> for InputError {
    fn from(error: DomError) -> Self {
        Self::Dispatch(error)
    }
}

/// Routes pointer locations to event targets for one layout of one document.
///
/// Holds the layout it hit-tests and the epoch that layout was computed at.
/// Rebuild it whenever layout is recomputed; the epoch check will refuse
/// dispatches in the meantime rather than let them land somewhere plausible.
#[derive(Debug)]
pub struct HitRouter {
    layout: LayoutBox,
    computed_at: Epoch,
}

impl HitRouter {
    /// Captures `layout` as the geometry of `dom` as it currently stands.
    ///
    /// The epoch is read here rather than at dispatch, because here is the only
    /// moment the two are known to agree.
    #[must_use]
    pub fn new(dom: &Dom, layout: LayoutBox) -> Self {
        Self {
            layout,
            computed_at: dom.epoch(),
        }
    }

    /// Returns the epoch this router's layout was computed at.
    #[must_use]
    pub const fn computed_at(&self) -> Epoch {
        self.computed_at
    }

    /// Returns the node at `point`, without dispatching.
    ///
    /// # Errors
    ///
    /// Returns [`InputError::LayoutOutOfDate`] if the document has changed since
    /// the layout was captured.
    pub fn target_at(&self, dom: &Dom, point: Point) -> Result<Option<NodeId>, InputError> {
        self.check_current(dom)?;
        Ok(hit_test(&self.layout, point).map(NodeId::from_index))
    }

    /// Dispatches `event` to whatever is at `point`.
    ///
    /// Returns `Ok(None)` when nothing is there. That is an answer rather than a
    /// failure: a click on empty space outside the document's boxes has no
    /// target, and inventing one — the root is the tempting choice — would
    /// deliver events nobody aimed at anything.
    ///
    /// # Errors
    ///
    /// Returns [`InputError::LayoutOutOfDate`] if the document changed after the
    /// layout was captured, or [`InputError::Dispatch`] if the DOM refuses.
    pub fn dispatch_at(
        &self,
        dom: &Dom,
        point: Point,
        event: &Event,
    ) -> Result<Option<Dispatch>, InputError> {
        let Some(node) = self.target_at(dom, point)? else {
            return Ok(None);
        };
        // Safe to mint now: the epoch check above established that the document
        // has not moved since layout, so the current epoch is the layout's.
        let handle = dom.handle(node);
        Ok(Some(dom.dispatch(handle, event)?))
    }

    fn check_current(&self, dom: &Dom) -> Result<(), InputError> {
        let current = dom.epoch();
        if current == self.computed_at {
            return Ok(());
        }
        Err(InputError::LayoutOutOfDate {
            computed_at: self.computed_at,
            current,
        })
    }
}
