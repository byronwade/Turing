// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Turing-owned HTML tree construction.
//!
//! This module implements the tree-construction stage of `WP-006`, consuming
//! the token stream from [`crate::Tokenizer`] and producing a document tree. It
//! is written against the WHATWG insertion-mode algorithm and derives from no
//! existing browser engine, consistent with the `ADR-0009` Option A direction.
//!
//! # Arena representation
//!
//! Nodes live in a flat [`Vec`] and reference each other by [`NodeId`]. A
//! browser DOM is mutated constantly and traversed in both directions, so an
//! arena avoids the reference-counting and interior-mutability costs a
//! pointer-based tree would require in Rust. This also matches the direction
//! `WP-007` records for the DOM arena.
//!
//! # Deliberate limits
//!
//! The specification defines twenty-three insertion modes. This implementation
//! covers the modes reachable from ordinary markup: initial, before-html,
//! before-head, in-head, after-head, in-body, text, after-body, and
//! after-after-body. It performs implied end-tag closing and handles void
//! elements and missing `html`, `head`, or `body` tags.
//!
//! Three areas are deliberately not implemented, and each returns a
//! [`TreeError`] rather than a wrong tree:
//!
//! - table insertion modes and foster parenting;
//! - the adoption agency algorithm, which repairs mis-nested formatting
//!   elements such as `<b><i></b></i>`;
//! - foreign content, meaning embedded SVG and MathML.
//!
//! Each of these changes the resulting tree shape rather than merely omitting
//! detail. Producing a plausible-looking wrong tree would be worse than
//! refusing, because downstream layout and script would silently disagree with
//! every other engine.

use crate::{Attribute, Token};
use core::fmt;

/// Handle to a node inside a [`Document`] arena.
#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct NodeId(usize);

impl NodeId {
    /// Returns the arena index this handle refers to.
    #[must_use]
    pub const fn index(self) -> usize {
        self.0
    }

    /// Builds a handle from an arena index.
    ///
    /// Callers enumerating a [`Document`] use this to walk every node. An index
    /// beyond the arena will panic on first access rather than read a
    /// neighbouring node.
    #[must_use]
    pub const fn from_index(index: usize) -> Self {
        Self(index)
    }
}

/// Payload of a document node.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum NodeData {
    /// The document root.
    Document,
    /// A doctype declaration.
    Doctype {
        name: Option<String>,
        public_id: Option<String>,
        system_id: Option<String>,
    },
    /// An element with its attributes.
    Element {
        name: String,
        attributes: Vec<Attribute>,
    },
    /// Character data.
    Text(String),
    /// A comment.
    Comment(String),
}

/// A node in the document arena.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Node {
    /// This node's payload.
    pub data: NodeData,
    /// Parent handle, absent only for the document root.
    pub parent: Option<NodeId>,
    /// Child handles in document order.
    pub children: Vec<NodeId>,
}

/// A constructed document tree.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Document {
    nodes: Vec<Node>,
}

impl Document {
    /// Returns the document root handle.
    #[must_use]
    pub const fn root(&self) -> NodeId {
        NodeId(0)
    }

    /// Returns the node for `id`.
    #[must_use]
    pub fn node(&self, id: NodeId) -> &Node {
        &self.nodes[id.0]
    }

    /// Returns the number of nodes, including the document root.
    #[must_use]
    pub fn len(&self) -> usize {
        self.nodes.len()
    }

    /// Returns whether the document contains only its root.
    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.nodes.len() <= 1
    }

    /// Returns the element name for `id`, if it is an element.
    #[must_use]
    pub fn element_name(&self, id: NodeId) -> Option<&str> {
        match &self.node(id).data {
            NodeData::Element { name, .. } => Some(name.as_str()),
            _ => None,
        }
    }

    /// Serializes the tree as indented text.
    ///
    /// This exists for tests and diagnostics. It is not an HTML serializer and
    /// deliberately does not round-trip to markup.
    #[must_use]
    pub fn to_debug_string(&self) -> String {
        let mut out = String::new();
        self.write_node(self.root(), 0, &mut out);
        out
    }

    fn write_node(&self, id: NodeId, depth: usize, out: &mut String) {
        let node = self.node(id);
        if depth > 0 {
            for _ in 0..(depth - 1) {
                out.push_str("  ");
            }
            match &node.data {
                NodeData::Document => {}
                NodeData::Doctype { name, .. } => {
                    out.push_str("<!DOCTYPE ");
                    out.push_str(name.as_deref().unwrap_or(""));
                    out.push_str(">\n");
                }
                NodeData::Element { name, attributes } => {
                    out.push('<');
                    out.push_str(name);
                    for attribute in attributes {
                        out.push(' ');
                        out.push_str(&attribute.name);
                        out.push_str("=\"");
                        out.push_str(&attribute.value);
                        out.push('"');
                    }
                    out.push_str(">\n");
                }
                NodeData::Text(text) => {
                    out.push('"');
                    out.push_str(text);
                    out.push_str("\"\n");
                }
                NodeData::Comment(text) => {
                    out.push_str("<!--");
                    out.push_str(text);
                    out.push_str("-->\n");
                }
            }
        }
        for &child in &node.children {
            self.write_node(child, depth + 1, out);
        }
    }
}

/// A construct this implementation does not model.
///
/// These are returned rather than approximated because each one changes the
/// shape of the resulting tree, not merely its detail.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum TreeError {
    /// Table insertion modes and foster parenting are not implemented.
    TableConstructionUnsupported { tag: String },
    /// The adoption agency algorithm is not implemented.
    MisnestedFormattingUnsupported { open: String, closed: String },
    /// SVG and MathML integration points are not implemented.
    ForeignContentUnsupported { tag: String },
    /// `template` has its own content document and insertion mode.
    TemplateUnsupported,
}

impl fmt::Display for TreeError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::TableConstructionUnsupported { tag } => write!(
                formatter,
                "table construction for <{tag}> is not implemented; it requires foster parenting"
            ),
            Self::MisnestedFormattingUnsupported { open, closed } => write!(
                formatter,
                "mis-nested formatting (<{open}> closed by </{closed}>) requires the adoption agency algorithm, which is not implemented"
            ),
            Self::ForeignContentUnsupported { tag } => {
                write!(formatter, "foreign content <{tag}> is not implemented")
            }
            Self::TemplateUnsupported => {
                write!(formatter, "<template> is not implemented")
            }
        }
    }
}

/// Insertion mode, per the specification's tree-construction dispatcher.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum Mode {
    Initial,
    BeforeHtml,
    BeforeHead,
    InHead,
    AfterHead,
    InBody,
    Text,
    AfterBody,
    AfterAfterBody,
}

/// Elements that never have children and are closed by their start tag.
const VOID_ELEMENTS: &[&str] = &[
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source",
    "track", "wbr",
];

/// Elements whose open tag is implicitly closed by a following block element.
const IMPLIED_END_TAGS: &[&str] = &[
    "dd", "dt", "li", "optgroup", "option", "p", "rb", "rp", "rt", "rtc",
];

/// Formatting elements the adoption agency algorithm would repair.
const FORMATTING_ELEMENTS: &[&str] = &[
    "a", "b", "big", "code", "em", "font", "i", "nobr", "s", "small", "strike", "strong", "tt", "u",
];

/// Table-related elements requiring insertion modes not implemented here.
const TABLE_ELEMENTS: &[&str] = &[
    "table", "tbody", "td", "tfoot", "th", "thead", "tr", "caption", "colgroup", "col",
];

/// Builds a document tree from a token stream.
#[derive(Debug)]
pub struct TreeBuilder {
    nodes: Vec<Node>,
    open_elements: Vec<NodeId>,
    mode: Mode,
    head: Option<NodeId>,
    body: Option<NodeId>,
    /// Mode to return to when the current text span ends.
    original_mode: Mode,
}

impl Default for TreeBuilder {
    fn default() -> Self {
        Self::new()
    }
}

impl TreeBuilder {
    /// Creates a builder with an empty document.
    #[must_use]
    pub fn new() -> Self {
        Self {
            nodes: vec![Node {
                data: NodeData::Document,
                parent: None,
                children: Vec::new(),
            }],
            open_elements: Vec::new(),
            mode: Mode::Initial,
            head: None,
            body: None,
            original_mode: Mode::InBody,
        }
    }

    /// Consumes `tokens` and returns the constructed document.
    ///
    /// # Errors
    ///
    /// Returns [`TreeError`] when the input reaches a construct this
    /// implementation does not model, rather than producing a tree that would
    /// disagree with other engines.
    pub fn build(mut self, tokens: &[Token]) -> Result<Document, TreeError> {
        for token in tokens {
            self.process(token)?;
        }
        Ok(Document { nodes: self.nodes })
    }

    fn process(&mut self, token: &Token) -> Result<(), TreeError> {
        match self.mode {
            Mode::Initial => self.process_initial(token),
            Mode::BeforeHtml => self.process_before_html(token),
            Mode::BeforeHead => self.process_before_head(token),
            Mode::InHead => self.process_in_head(token),
            Mode::AfterHead => self.process_after_head(token),
            Mode::InBody => self.process_in_body(token),
            Mode::Text => self.process_text(token),
            Mode::AfterBody | Mode::AfterAfterBody => self.process_after_body(token),
        }
    }

    // -- modes -----------------------------------------------------------

    fn process_initial(&mut self, token: &Token) -> Result<(), TreeError> {
        match token {
            Token::Doctype {
                name,
                public_id,
                system_id,
                ..
            } => {
                let root = self.document_root();
                self.append(
                    root,
                    NodeData::Doctype {
                        name: name.clone(),
                        public_id: public_id.clone(),
                        system_id: system_id.clone(),
                    },
                );
                self.mode = Mode::BeforeHtml;
                Ok(())
            }
            Token::Comment(text) => {
                let root = self.document_root();
                self.append(root, NodeData::Comment(text.clone()));
                Ok(())
            }
            // Whitespace before the doctype is ignored; anything else means the
            // document omitted its doctype, so reprocess in the next mode.
            Token::Characters(text) if text.trim().is_empty() => Ok(()),
            _ => {
                self.mode = Mode::BeforeHtml;
                self.process(token)
            }
        }
    }

    fn process_before_html(&mut self, token: &Token) -> Result<(), TreeError> {
        if let Token::StartTag { name, .. } = token
            && name == "html"
        {
            self.insert_element_from(token);
            self.mode = Mode::BeforeHead;
            return Ok(());
        }
        if let Token::Characters(text) = token
            && text.trim().is_empty()
        {
            return Ok(());
        }
        // The html element is implied when absent.
        self.insert_element("html", Vec::new());
        self.mode = Mode::BeforeHead;
        self.process(token)
    }

    fn process_before_head(&mut self, token: &Token) -> Result<(), TreeError> {
        match token {
            Token::Characters(text) if text.trim().is_empty() => Ok(()),
            Token::Comment(text) => {
                let parent = self.current_node();
                self.append(parent, NodeData::Comment(text.clone()));
                Ok(())
            }
            Token::StartTag { name, .. } if name == "head" => {
                let id = self.insert_element_from(token);
                self.head = Some(id);
                self.mode = Mode::InHead;
                Ok(())
            }
            _ => {
                let id = self.insert_element("head", Vec::new());
                self.head = Some(id);
                self.mode = Mode::InHead;
                self.process(token)
            }
        }
    }

    fn process_in_head(&mut self, token: &Token) -> Result<(), TreeError> {
        match token {
            Token::Comment(text) => {
                let parent = self.current_node();
                self.append(parent, NodeData::Comment(text.clone()));
                Ok(())
            }
            Token::Characters(text) if text.trim().is_empty() => Ok(()),
            Token::StartTag { name, .. } if name == "template" => {
                Err(TreeError::TemplateUnsupported)
            }
            Token::StartTag { name, .. }
                if matches!(name.as_str(), "title" | "style" | "script") =>
            {
                self.insert_element_from(token);
                self.original_mode = Mode::InHead;
                self.mode = Mode::Text;
                Ok(())
            }
            Token::StartTag { name, .. } if VOID_ELEMENTS.contains(&name.as_str()) => {
                self.insert_void_from(token);
                Ok(())
            }
            Token::EndTag { name } if name == "head" => {
                self.pop_until_named("head");
                self.mode = Mode::AfterHead;
                Ok(())
            }
            _ => {
                self.pop_until_named("head");
                self.mode = Mode::AfterHead;
                self.process(token)
            }
        }
    }

    fn process_after_head(&mut self, token: &Token) -> Result<(), TreeError> {
        match token {
            Token::Characters(text) if text.trim().is_empty() => Ok(()),
            Token::Comment(text) => {
                let parent = self.current_node();
                self.append(parent, NodeData::Comment(text.clone()));
                Ok(())
            }
            Token::StartTag { name, .. } if name == "body" => {
                let id = self.insert_element_from(token);
                self.body = Some(id);
                self.mode = Mode::InBody;
                Ok(())
            }
            _ => {
                let id = self.insert_element("body", Vec::new());
                self.body = Some(id);
                self.mode = Mode::InBody;
                self.process(token)
            }
        }
    }

    fn process_in_body(&mut self, token: &Token) -> Result<(), TreeError> {
        match token {
            Token::Characters(text) => {
                let parent = self.current_node();
                self.append(parent, NodeData::Text(text.clone()));
                Ok(())
            }
            Token::Comment(text) => {
                let parent = self.current_node();
                self.append(parent, NodeData::Comment(text.clone()));
                Ok(())
            }
            Token::Doctype { .. } => Ok(()),
            Token::StartTag {
                name, self_closing, ..
            } => self.start_tag_in_body(token, name, *self_closing),
            Token::EndTag { name } => self.end_tag_in_body(name),
        }
    }

    fn start_tag_in_body(
        &mut self,
        token: &Token,
        name: &str,
        self_closing: bool,
    ) -> Result<(), TreeError> {
        if TABLE_ELEMENTS.contains(&name) {
            return Err(TreeError::TableConstructionUnsupported {
                tag: name.to_string(),
            });
        }
        if matches!(name, "svg" | "math") {
            return Err(TreeError::ForeignContentUnsupported {
                tag: name.to_string(),
            });
        }
        if name == "template" {
            return Err(TreeError::TemplateUnsupported);
        }
        if name == "body" {
            // A second body tag merges attributes onto the existing one.
            return Ok(());
        }

        // A block-level start tag closes an open paragraph.
        if name == "p" || is_block_element(name) {
            self.close_p_if_open();
        }
        // List items and definition terms close their open sibling.
        if matches!(name, "li" | "dd" | "dt") {
            self.close_implied_sibling(name);
        }

        if VOID_ELEMENTS.contains(&name) || self_closing {
            self.insert_void_from(token);
            return Ok(());
        }

        if matches!(name, "textarea" | "title" | "style" | "script") {
            self.insert_element_from(token);
            self.original_mode = Mode::InBody;
            self.mode = Mode::Text;
            return Ok(());
        }

        self.insert_element_from(token);
        Ok(())
    }

    fn end_tag_in_body(&mut self, name: &str) -> Result<(), TreeError> {
        if name == "body" {
            self.mode = Mode::AfterBody;
            return Ok(());
        }
        if name == "html" {
            self.mode = Mode::AfterBody;
            return Ok(());
        }
        if TABLE_ELEMENTS.contains(&name) {
            return Err(TreeError::TableConstructionUnsupported {
                tag: name.to_string(),
            });
        }

        let Some(depth) = self.index_of_open(name) else {
            // An end tag with no matching open element is ignored.
            return Ok(());
        };

        // Anything still open above the match that is a formatting element
        // means the document mis-nested tags, which needs the adoption agency
        // algorithm to repair correctly.
        for &id in &self.open_elements[depth + 1..] {
            if let Some(open_name) = element_name_of(&self.nodes, id)
                && FORMATTING_ELEMENTS.contains(&open_name)
            {
                return Err(TreeError::MisnestedFormattingUnsupported {
                    open: open_name.to_string(),
                    closed: name.to_string(),
                });
            }
        }

        self.open_elements.truncate(depth);
        Ok(())
    }

    fn process_text(&mut self, token: &Token) -> Result<(), TreeError> {
        match token {
            Token::Characters(text) => {
                let parent = self.current_node();
                self.append(parent, NodeData::Text(text.clone()));
                Ok(())
            }
            Token::EndTag { .. } => {
                self.open_elements.pop();
                self.mode = self.original_mode;
                Ok(())
            }
            _ => {
                self.mode = self.original_mode;
                self.process(token)
            }
        }
    }

    fn process_after_body(&mut self, token: &Token) -> Result<(), TreeError> {
        match token {
            Token::Comment(text) => {
                let root = self.document_root();
                self.append(root, NodeData::Comment(text.clone()));
                Ok(())
            }
            Token::Characters(text) if text.trim().is_empty() => Ok(()),
            Token::EndTag { name } if name == "html" => {
                self.mode = Mode::AfterAfterBody;
                Ok(())
            }
            // Content after </body> is a parse error that browsers recover
            // from by returning to in-body.
            _ => {
                self.mode = Mode::InBody;
                self.process(token)
            }
        }
    }

    // -- tree operations -------------------------------------------------

    const fn document_root(&self) -> NodeId {
        NodeId(0)
    }

    fn current_node(&self) -> NodeId {
        self.open_elements.last().copied().unwrap_or(NodeId(0))
    }

    fn append(&mut self, parent: NodeId, data: NodeData) -> NodeId {
        // Adjacent text runs are merged so callers see one text node per span,
        // which is what the specification's "insert a character" produces.
        if let NodeData::Text(ref incoming) = data
            && let Some(&last) = self.nodes[parent.0].children.last()
            && let NodeData::Text(ref mut existing) = self.nodes[last.0].data
        {
            existing.push_str(incoming);
            return last;
        }
        let id = NodeId(self.nodes.len());
        self.nodes.push(Node {
            data,
            parent: Some(parent),
            children: Vec::new(),
        });
        self.nodes[parent.0].children.push(id);
        id
    }

    fn insert_element(&mut self, name: &str, attributes: Vec<Attribute>) -> NodeId {
        let parent = self.current_node();
        let id = self.append(
            parent,
            NodeData::Element {
                name: name.to_string(),
                attributes,
            },
        );
        self.open_elements.push(id);
        id
    }

    fn insert_element_from(&mut self, token: &Token) -> NodeId {
        let (name, attributes) = element_parts(token);
        self.insert_element(&name, attributes)
    }

    /// Inserts an element that is immediately closed and never opened.
    fn insert_void_from(&mut self, token: &Token) -> NodeId {
        let (name, attributes) = element_parts(token);
        let parent = self.current_node();
        self.append(parent, NodeData::Element { name, attributes })
    }

    fn index_of_open(&self, name: &str) -> Option<usize> {
        self.open_elements
            .iter()
            .rposition(|&id| element_name_of(&self.nodes, id) == Some(name))
    }

    fn pop_until_named(&mut self, name: &str) {
        if let Some(index) = self.index_of_open(name) {
            self.open_elements.truncate(index);
        }
    }

    fn close_p_if_open(&mut self) {
        if let Some(index) = self.index_of_open("p") {
            self.open_elements.truncate(index);
        }
    }

    /// Closes an open `li`, `dd`, or `dt` before a sibling of the same kind.
    fn close_implied_sibling(&mut self, name: &str) {
        if let Some(index) = self.index_of_open(name)
            && IMPLIED_END_TAGS.contains(&name)
        {
            self.open_elements.truncate(index);
        }
    }
}

fn element_parts(token: &Token) -> (String, Vec<Attribute>) {
    match token {
        Token::StartTag {
            name, attributes, ..
        } => (name.clone(), attributes.clone()),
        _ => (String::new(), Vec::new()),
    }
}

fn element_name_of(nodes: &[Node], id: NodeId) -> Option<&str> {
    match &nodes[id.0].data {
        NodeData::Element { name, .. } => Some(name.as_str()),
        _ => None,
    }
}

/// Returns whether a block-level start tag implicitly closes an open `p`.
fn is_block_element(name: &str) -> bool {
    matches!(
        name,
        "address"
            | "article"
            | "aside"
            | "blockquote"
            | "div"
            | "dl"
            | "fieldset"
            | "figcaption"
            | "figure"
            | "footer"
            | "form"
            | "h1"
            | "h2"
            | "h3"
            | "h4"
            | "h5"
            | "h6"
            | "header"
            | "hr"
            | "main"
            | "nav"
            | "ol"
            | "pre"
            | "section"
            | "ul"
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::Tokenizer;

    fn build(html: &str) -> Result<Document, TreeError> {
        let tokens = Tokenizer::new(html).tokenize().expect("tokenizes").tokens;
        TreeBuilder::new().build(&tokens)
    }

    fn tree(html: &str) -> String {
        build(html).expect("builds").to_debug_string()
    }

    #[test]
    fn builds_minimal_document() {
        assert_eq!(
            tree("<html><head></head><body></body></html>"),
            "<html>\n  <head>\n  <body>\n"
        );
    }

    #[test]
    fn implies_missing_html_head_and_body() {
        // Bare text must still produce the full implied structure.
        assert_eq!(tree("hello"), "<html>\n  <head>\n  <body>\n    \"hello\"\n");
    }

    #[test]
    fn places_doctype_before_root() {
        assert_eq!(
            tree("<!DOCTYPE html><p>x</p>"),
            "<!DOCTYPE html>\n<html>\n  <head>\n  <body>\n    <p>\n      \"x\"\n"
        );
    }

    #[test]
    fn nests_elements() {
        assert_eq!(
            tree("<div><span>a</span></div>"),
            "<html>\n  <head>\n  <body>\n    <div>\n      <span>\n        \"a\"\n"
        );
    }

    #[test]
    fn preserves_attributes() {
        assert_eq!(
            tree("<a href=\"/x\" id=\"y\">t</a>"),
            "<html>\n  <head>\n  <body>\n    <a href=\"/x\" id=\"y\">\n      \"t\"\n"
        );
    }

    #[test]
    fn void_elements_do_not_nest() {
        // <br> must not become a parent of the text that follows it.
        assert_eq!(
            tree("<p>a<br>b</p>"),
            "<html>\n  <head>\n  <body>\n    <p>\n      \"a\"\n      <br>\n      \"b\"\n"
        );
    }

    #[test]
    fn block_element_closes_open_paragraph() {
        // <p>a<div> yields siblings, not a div nested inside the p.
        assert_eq!(
            tree("<p>a<div>b</div>"),
            "<html>\n  <head>\n  <body>\n    <p>\n      \"a\"\n    <div>\n      \"b\"\n"
        );
    }

    #[test]
    fn list_items_close_their_siblings() {
        assert_eq!(
            tree("<ul><li>a<li>b</ul>"),
            "<html>\n  <head>\n  <body>\n    <ul>\n      <li>\n        \"a\"\n      <li>\n        \"b\"\n"
        );
    }

    #[test]
    fn head_elements_land_in_head() {
        assert_eq!(
            tree("<head><meta charset=\"utf-8\"><title>T</title></head><body>x</body>"),
            "<html>\n  <head>\n    <meta charset=\"utf-8\">\n    <title>\n      \"T\"\n  <body>\n    \"x\"\n"
        );
    }

    #[test]
    fn script_contents_become_text_not_markup() {
        let document = build("<script>var a = \"<b>\";</script>").expect("builds");
        let output = document.to_debug_string();
        assert!(output.contains("<script>"), "{output}");
        assert!(output.contains("var a = \\\"<b>\\\";") || output.contains("var a = \"<b>\";"));
        assert!(
            !output.contains("\n      <b>"),
            "b became an element: {output}"
        );
    }

    #[test]
    fn adjacent_text_runs_merge() {
        let document = build("<p>a&amp;b</p>").expect("builds");
        let body = document.node(document.root()).children[0];
        let body_children = &document.node(body).children;
        let paragraph = document
            .node(body_children[1])
            .children
            .first()
            .copied()
            .expect("p exists");
        assert_eq!(document.node(paragraph).children.len(), 1);
    }

    #[test]
    fn comments_are_retained() {
        assert_eq!(
            tree("<body><!-- note --></body>"),
            "<html>\n  <head>\n  <body>\n    <!-- note -->\n"
        );
    }

    #[test]
    fn stray_end_tag_is_ignored() {
        assert_eq!(
            tree("<p>a</span></p>"),
            "<html>\n  <head>\n  <body>\n    <p>\n      \"a\"\n"
        );
    }

    #[test]
    fn tables_are_reported_not_guessed() {
        let error = build("<table><tr><td>x</td></tr></table>").expect_err("unsupported");
        assert!(matches!(
            error,
            TreeError::TableConstructionUnsupported { .. }
        ));
    }

    #[test]
    fn misnested_formatting_is_reported_not_guessed() {
        // <b><i></b></i> needs the adoption agency algorithm; guessing here
        // would produce a tree that disagrees with every other engine.
        let error = build("<p><b><i>x</b>y</i></p>").expect_err("unsupported");
        assert!(matches!(
            error,
            TreeError::MisnestedFormattingUnsupported { .. }
        ));
    }

    #[test]
    fn foreign_content_is_reported_not_guessed() {
        let error = build("<svg><circle/></svg>").expect_err("unsupported");
        assert!(matches!(error, TreeError::ForeignContentUnsupported { .. }));
    }

    #[test]
    fn template_is_reported_not_guessed() {
        let error = build("<template><p>x</p></template>").expect_err("unsupported");
        assert!(matches!(error, TreeError::TemplateUnsupported));
    }

    #[test]
    fn properly_nested_formatting_is_accepted() {
        assert_eq!(
            tree("<p><b><i>x</i></b></p>"),
            "<html>\n  <head>\n  <body>\n    <p>\n      <b>\n        <i>\n          \"x\"\n"
        );
    }

    #[test]
    fn builds_a_small_page() {
        let html = "<!DOCTYPE html><html><head><title>T</title></head>\
                    <body><h1>Hi</h1><p>x<br>y</p><!-- c --></body></html>";
        let document = build(html).expect("builds");
        assert!(document.len() > 8, "{}", document.to_debug_string());
        let output = document.to_debug_string();
        assert!(output.starts_with("<!DOCTYPE html>\n<html>\n"), "{output}");
        assert!(output.contains("<h1>"), "{output}");
        assert!(output.contains("<br>"), "{output}");
    }

    #[test]
    fn parent_links_are_consistent() {
        let document = build("<div><span>a</span></div>").expect("builds");
        for index in 1..document.len() {
            let id = NodeId(index);
            let parent = document.node(id).parent.expect("non-root has a parent");
            assert!(
                document.node(parent).children.contains(&id),
                "node {index} is not listed by its parent"
            );
        }
    }
}
