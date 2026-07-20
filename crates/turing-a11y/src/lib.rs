// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Turing-owned accessibility tree derived from document semantics.
//!
//! This crate implements `REQ-ENG-006`, the remaining piece of `WP-009`. It is
//! written from ARIA, HTML-AAM, and the Accessible Name and Description
//! Computation, deriving from no existing engine, consistent with `ADR-0009`
//! Option A.
//!
//! # Derived, not scraped
//!
//! The tree is computed from elements and attributes, never from pixels or from
//! layout geometry. That is why this crate depends on an element tree rather
//! than on `turing-layout`: an element's role and name do not change because it
//! moved, and coupling the two would make accessibility a rendering artifact.
//!
//! # Order of operations
//!
//! Role is resolved *before* name, and this ordering is load-bearing rather
//! than incidental. Whether an element takes its name from its descendant text
//! is a property of its role — a button does, a text box does not — so
//! computing the name first would have to guess.
//!
//! # Deliberate limits
//!
//! This is a bounded slice. Elements outside the mapped set, and explicit
//! `role` tokens outside the modelled set, return a typed error rather than
//! falling back to a generic role. A wrong role is not a cosmetic defect: it
//! changes how an assistive technology announces, navigates, and offers actions
//! on the element, and it does so invisibly to anyone not using one.
//!
//! Not modelled, each returning [`A11yError`] rather than a guess:
//!
//! - the `<label for>` association, and `<fieldset>`/`<legend>`, which name a
//!   control from an element elsewhere in the document;
//! - table semantics, live regions, and `<dialog>`;
//! - states and properties beyond name — value, checked, expanded, disabled;
//! - descriptions, which have their own precedence chain.

#![forbid(unsafe_code)]

use core::fmt;
use turing_css::ElementTree;

/// What the accessibility tree needs from a document beyond element matching.
///
/// [`element_by_id`](SemanticTree::element_by_id) is the reason this is a
/// separate trait rather than a reuse of the layout one: `aria-labelledby`
/// resolves references against the whole document, which no amount of local
/// walking can express.
pub trait SemanticTree: ElementTree {
    /// Returns the root node.
    fn root(&self) -> Self::Node;

    /// Returns the node's children in document order.
    fn children(&self, node: Self::Node) -> Vec<Self::Node>;

    /// Returns the node's text, if it is a text node.
    fn text(&self, node: Self::Node) -> Option<&str>;

    /// Returns the element whose `id` attribute equals `id`.
    ///
    /// Document-global by nature. When several elements share an `id` the
    /// document is malformed; returning the first in document order matches
    /// what `getElementById` is specified to do.
    fn element_by_id(&self, id: &str) -> Option<Self::Node>;

    /// Returns a stable index identifying the node, so a caller can map a
    /// result back into their own tree.
    fn node_index(&self, node: Self::Node) -> usize;
}

/// A construct this implementation does not model.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum A11yError {
    /// An element with no mapping in the modelled set.
    ElementNotMapped { tag: String },
    /// An explicit `role` token this implementation does not model.
    RoleUnsupported { role: String },
    /// The element's name would come from a source that is not implemented.
    NameSourceUnsupported { tag: String, source: String },
    /// The document nests deeper than this implementation will recurse.
    NestingTooDeep { limit: usize },
}

impl fmt::Display for A11yError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::ElementNotMapped { tag } => write!(
                formatter,
                "<{tag}> has no role mapping here; guessing a generic role would \
                 change how assistive technology announces and navigates it"
            ),
            Self::RoleUnsupported { role } => write!(
                formatter,
                "role=\"{role}\" is not modelled; its name-from-content and \
                 required-children behaviour would have to be invented"
            ),
            Self::NestingTooDeep { limit } => write!(
                formatter,
                "the document nests deeper than {limit} elements; tree construction                  recurses, and continuing would overflow the stack, which aborts the                  process rather than returning an error"
            ),
            Self::NameSourceUnsupported { tag, source } => write!(
                formatter,
                "<{tag}> would take its accessible name from {source}, which is \
                 not implemented; reporting no name would hide a named control"
            ),
        }
    }
}

/// The deepest element nesting this implementation will walk.
///
/// Matches `turing_layout::MAX_NESTING_DEPTH` deliberately: two consumers of the
/// same document disagreeing about which documents are acceptable would mean a
/// page that lays out but has no accessibility tree, or the reverse.
pub const MAX_NESTING_DEPTH: usize = 256;

/// A computed role.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum Role {
    Button,
    Link,
    Heading {
        level: u8,
    },
    Paragraph,
    List,
    ListItem,
    Navigation,
    Main,
    /// `<header>` scoped to the body, or `role="banner"`.
    Banner,
    /// `<footer>` scoped to the body, or `role="contentinfo"`.
    ContentInfo,
    Complementary,
    Image,
    Textbox,
    Checkbox,
    /// An element with no semantics of its own, such as `<div>`.
    Generic,
    /// The document root.
    Document,
}

impl Role {
    /// Whether this role takes its accessible name from descendant text.
    ///
    /// A property of the role, not of the element. Concatenating descendant
    /// text for everything is the classic quiet defect here: it gives a text
    /// box the name of whatever happens to sit inside it, which sounds
    /// plausible when read in a test and is wrong in use.
    #[must_use]
    pub fn names_from_content(&self) -> bool {
        matches!(
            self,
            Self::Button | Self::Link | Self::Heading { .. } | Self::Checkbox
        )
    }
}

/// One node of the accessibility tree.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct AccessibilityNode {
    pub role: Role,
    /// The accessible name, absent when the element has none.
    pub name: Option<String>,
    /// Index of the source element, for mapping back into the host tree.
    pub node: usize,
    pub children: Vec<AccessibilityNode>,
}

/// Builds the accessibility tree for `tree`.
///
/// # Errors
///
/// Returns [`A11yError`] when the document contains an element or role this
/// implementation does not model, rather than exposing it with a guessed role.
pub fn build<T: SemanticTree>(tree: &T) -> Result<AccessibilityNode, A11yError> {
    let root = tree.root();
    let children = build_children(tree, root, 0)?;
    Ok(AccessibilityNode {
        role: Role::Document,
        name: None,
        node: tree.node_index(root),
        children,
    })
}

fn build_children<T: SemanticTree>(
    tree: &T,
    node: T::Node,
    depth: usize,
) -> Result<Vec<AccessibilityNode>, A11yError> {
    let mut exposed = Vec::new();
    for child in tree.children(node) {
        exposed.extend(build_node(tree, child, depth)?);
    }
    Ok(exposed)
}

/// Builds zero or more accessibility nodes for one source node.
///
/// Zero when the element is hidden or is not exposed at all; more than one when
/// the element itself is presentational but its children remain exposed.
fn build_node<T: SemanticTree>(
    tree: &T,
    node: T::Node,
    depth: usize,
) -> Result<Vec<AccessibilityNode>, A11yError> {
    // Tree construction recurses on document depth. A stack overflow aborts the
    // process and cannot be caught, so a document deeper than the limit is
    // refused rather than allowed to crash.
    if depth > MAX_NESTING_DEPTH {
        return Err(A11yError::NestingTooDeep {
            limit: MAX_NESTING_DEPTH,
        });
    }

    if !tree.is_element(node) {
        // Text contributes to names, not to structure.
        return Ok(Vec::new());
    }

    // `aria-hidden="true"` removes the element *and its subtree*. This is
    // distinct from `role="presentation"`, which strips only the element's own
    // semantics; conflating the two is the standard mistake, and it fails in
    // opposite directions — one over-exposes, the other hides real content.
    if tree.attribute(node, "aria-hidden") == Some("true") {
        return Ok(Vec::new());
    }

    let tag = tree.tag_name(node).unwrap_or_default().to_string();

    // Elements that structure the document without appearing in the tree.
    if matches!(tag.as_str(), "html" | "head" | "body") {
        return build_children(tree, node, depth + 1);
    }
    if matches!(tag.as_str(), "title" | "style" | "script" | "meta" | "link") {
        return Ok(Vec::new());
    }

    let explicit = tree.attribute(node, "role").map(str::to_string);
    if let Some(role) = explicit.as_deref() {
        // `presentation` and `none` are synonyms: drop this element's
        // semantics, keep its children exposed.
        if matches!(role, "presentation" | "none") {
            return build_children(tree, node, depth + 1);
        }
    }

    let role = match explicit.as_deref() {
        Some(role) => explicit_role(role)?,
        None => implicit_role(tree, node, &tag)?,
    };

    // An `<img>` with an empty `alt` is explicitly marked decorative by its
    // author, which is a statement about the image and not a missing name.
    if tag == "img" && tree.attribute(node, "alt") == Some("") && explicit.is_none() {
        return Ok(Vec::new());
    }

    let name = accessible_name(tree, node, &role, &tag)?;

    Ok(vec![AccessibilityNode {
        role,
        name,
        node: tree.node_index(node),
        children: build_children(tree, node, depth + 1)?,
    }])
}

/// Maps an explicit `role` token.
///
/// An unmodelled token is refused rather than falling through to the implicit
/// role. ARIA does specify that fallback for *invalid* tokens, but this
/// implementation cannot tell an invalid token from a valid one it has not
/// modelled without carrying the full role taxonomy, and silently treating
/// `role="tablist"` as a `<div>` would be a wrong answer that reads as correct.
fn explicit_role(role: &str) -> Result<Role, A11yError> {
    Ok(match role {
        "button" => Role::Button,
        "link" => Role::Link,
        "heading" => Role::Heading { level: 2 },
        "paragraph" => Role::Paragraph,
        "list" => Role::List,
        "listitem" => Role::ListItem,
        "navigation" => Role::Navigation,
        "main" => Role::Main,
        "banner" => Role::Banner,
        "contentinfo" => Role::ContentInfo,
        "complementary" => Role::Complementary,
        "img" | "image" => Role::Image,
        "textbox" => Role::Textbox,
        "checkbox" => Role::Checkbox,
        "generic" => Role::Generic,
        other => {
            return Err(A11yError::RoleUnsupported {
                role: other.to_string(),
            });
        }
    })
}

/// Maps an element to its implicit role, per HTML-AAM.
fn implicit_role<T: SemanticTree>(tree: &T, node: T::Node, tag: &str) -> Result<Role, A11yError> {
    Ok(match tag {
        "button" => Role::Button,
        // An anchor is a link only when it has an `href`. Without one it has no
        // link semantics and is not focusable, so announcing it as a link would
        // offer an action that does not exist.
        "a" => {
            if tree.attribute(node, "href").is_some() {
                Role::Link
            } else {
                Role::Generic
            }
        }
        "h1" => Role::Heading { level: 1 },
        "h2" => Role::Heading { level: 2 },
        "h3" => Role::Heading { level: 3 },
        "h4" => Role::Heading { level: 4 },
        "h5" => Role::Heading { level: 5 },
        "h6" => Role::Heading { level: 6 },
        "p" => Role::Paragraph,
        "ul" | "ol" => Role::List,
        "li" => Role::ListItem,
        "nav" => Role::Navigation,
        "main" => Role::Main,
        // `<header>` and `<footer>` are landmarks only when scoped to the body.
        // Nested inside a sectioning element they are that section's header,
        // not the page's, and exposing a per-article header as the page banner
        // would put a landmark on every article in a feed.
        "header" => {
            if scoped_to_body(tree, node) {
                Role::Banner
            } else {
                Role::Generic
            }
        }
        "footer" => {
            if scoped_to_body(tree, node) {
                Role::ContentInfo
            } else {
                Role::Generic
            }
        }
        "aside" => Role::Complementary,
        "img" => Role::Image,
        "input" => input_role(tree, node)?,
        "div" | "span" => Role::Generic,
        other => {
            return Err(A11yError::ElementNotMapped {
                tag: other.to_string(),
            });
        }
    })
}

/// Whether the element has no sectioning ancestor between it and the body.
fn scoped_to_body<T: SemanticTree>(tree: &T, node: T::Node) -> bool {
    let mut current = tree.parent(node);
    while let Some(ancestor) = current {
        if let Some(tag) = tree.tag_name(ancestor)
            && matches!(tag, "article" | "aside" | "main" | "nav" | "section")
        {
            return false;
        }
        current = tree.parent(ancestor);
    }
    true
}

fn input_role<T: SemanticTree>(tree: &T, node: T::Node) -> Result<Role, A11yError> {
    // A missing `type` defaults to `text`.
    match tree.attribute(node, "type").unwrap_or("text") {
        "text" => Ok(Role::Textbox),
        "checkbox" => Ok(Role::Checkbox),
        "button" | "submit" | "reset" => Ok(Role::Button),
        other => Err(A11yError::RoleUnsupported {
            role: format!("input type={other}"),
        }),
    }
}

// -- accessible name -----------------------------------------------------

/// Computes the accessible name, in the precedence order the specification
/// defines.
///
/// The order is `aria-labelledby`, then `aria-label`, then the host-language
/// source, then name-from-content when the role allows it, then `title`. Each
/// rung must be tried only when every higher one is absent; an implementation
/// that checks them in a different order produces a plausible name from the
/// wrong source, which no test that supplies a single source will catch.
fn accessible_name<T: SemanticTree>(
    tree: &T,
    node: T::Node,
    role: &Role,
    tag: &str,
) -> Result<Option<String>, A11yError> {
    if let Some(reference) = tree.attribute(node, "aria-labelledby") {
        let mut visited = Vec::new();
        let name = name_from_references(tree, reference, &mut visited);
        if !name.is_empty() {
            return Ok(Some(name));
        }
    }

    if let Some(label) = tree.attribute(node, "aria-label") {
        let label = label.trim();
        if !label.is_empty() {
            return Ok(Some(label.to_string()));
        }
    }

    // Host-language sources.
    if tag == "img" {
        return Ok(tree
            .attribute(node, "alt")
            .map(str::trim)
            .filter(|alt| !alt.is_empty())
            .map(str::to_string)
            .or_else(|| title_of(tree, node)));
    }
    if tag == "input" {
        // A `<label for>` elsewhere in the document is the usual way a control
        // is named. Detecting its absence needs a document-wide scan this
        // implementation does not do, so a control with no ARIA name is refused
        // rather than reported as unnamed — an unnamed control and a control
        // whose name was not found are very different findings.
        if let Some(title) = title_of(tree, node) {
            return Ok(Some(title));
        }
        return Err(A11yError::NameSourceUnsupported {
            tag: tag.to_string(),
            source: "an associated <label for> element".to_string(),
        });
    }

    if role.names_from_content() {
        let content = descendant_text(tree, node);
        if !content.is_empty() {
            return Ok(Some(content));
        }
    }

    Ok(title_of(tree, node))
}

fn title_of<T: SemanticTree>(tree: &T, node: T::Node) -> Option<String> {
    tree.attribute(node, "title")
        .map(str::trim)
        .filter(|title| !title.is_empty())
        .map(str::to_string)
}

/// Resolves a space-separated `aria-labelledby` IDREF list.
///
/// `visited` is threaded through from the first call rather than added later,
/// because `aria-labelledby` can form a cycle — directly, or through a target
/// that contains the origin. Without the visited set a crafted document
/// recurses until the stack is exhausted, which is a denial of service reachable
/// from ordinary page content.
///
/// A reference to a missing element contributes nothing, which is what the
/// specification requires; it is an authoring error rather than an engine one.
fn name_from_references<T: SemanticTree>(
    tree: &T,
    reference: &str,
    visited: &mut Vec<usize>,
) -> String {
    let mut parts = Vec::new();
    for id in reference.split_whitespace() {
        let Some(target) = tree.element_by_id(id) else {
            continue;
        };
        let index = tree.node_index(target);
        if visited.contains(&index) {
            continue;
        }
        visited.push(index);

        // A target's own `aria-labelledby` is not followed recursively: the
        // specification allows only one level of indirection, so the target
        // contributes its text content. Following it would let a chain of
        // labels produce a name no element actually carries.
        let text = descendant_text(tree, target);
        if !text.is_empty() {
            parts.push(text);
        }
    }
    parts.join(" ")
}

/// Concatenates the text of a node's descendants, in document order.
fn descendant_text<T: SemanticTree>(tree: &T, node: T::Node) -> String {
    let mut parts = Vec::new();
    collect_text(tree, node, &mut parts);
    parts.join(" ")
}

/// Walks a subtree iteratively rather than recursively.
///
/// Name computation runs before the depth check reaches the deeper elements, so
/// this can be called on a subtree of any depth even when the tree as a whole
/// will be refused. An explicit stack means that cannot overflow — the same
/// reason `turing-gc` traces iteratively.
fn collect_text<T: SemanticTree>(tree: &T, node: T::Node, parts: &mut Vec<String>) {
    let mut stack = vec![node];
    while let Some(current) = stack.pop() {
        // A hidden subtree contributes nothing to a name, the same way it
        // contributes nothing to the tree.
        if tree.is_element(current) && tree.attribute(current, "aria-hidden") == Some("true") {
            continue;
        }
        if let Some(text) = tree.text(current) {
            let text = text.trim();
            if !text.is_empty() {
                parts.push(text.to_string());
            }
        }
        // Reversed, because popping from a stack visits the last push first and
        // a name must read in document order.
        stack.extend(tree.children(current).into_iter().rev());
    }
}

// -- turing-html adapter -------------------------------------------------

/// Implements [`SemanticTree`] for the engine's own document.
///
/// Behind the `html` feature, so the accessibility tree itself carries no
/// dependency on the DOM. This is also the shape an embedder copies.
#[cfg(feature = "html")]
mod html_tree {
    use super::SemanticTree;
    use turing_html::{Document, NodeData};

    impl SemanticTree for Document {
        fn root(&self) -> Self::Node {
            Document::root(self)
        }

        fn children(&self, node: Self::Node) -> Vec<Self::Node> {
            self.node(node).children.clone()
        }

        fn text(&self, node: Self::Node) -> Option<&str> {
            match &self.node(node).data {
                NodeData::Text(text) => Some(text.as_str()),
                _ => None,
            }
        }

        fn element_by_id(&self, id: &str) -> Option<Self::Node> {
            // Constant time: the document maintains the map. This was a linear
            // scan, which made resolving a list of aria-labelledby references
            // quadratic in document size.
            Document::element_by_id(self, id)
        }

        fn node_index(&self, node: Self::Node) -> usize {
            node.index()
        }
    }
}
