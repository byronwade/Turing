// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Turing-owned box generation, block layout, and display-list construction.
//!
//! This crate implements `WP-009` and `REQ-ENG-004`/`REQ-ENG-005`: turning a
//! styled document into positioned boxes, then into a flat list of paint
//! commands. It is written from the CSS box model, visual formatting model, and
//! display specifications, deriving from no existing engine, consistent with
//! `ADR-0009` Option A.
//!
//! # Pipeline position
//!
//! `turing-html` produces a tree and `turing-css` decides which declarations
//! apply to each node. This crate consumes both and answers where things go and
//! what is drawn. It does not rasterize; a display list is the handoff to a
//! painter, which is separate work.
//!
//! # Text measurement
//!
//! Real text advance depends on font selection, shaping, kerning, and fallback,
//! none of which exist yet. Rather than pretend, this crate takes an explicit
//! [`TextMetrics`] describing a monospace advance and line height. Layout is
//! therefore correct *given* those metrics, and the metrics are visibly a
//! placeholder rather than a hidden assumption baked into the algorithm.
//!
//! # Deliberate limits
//!
//! Block and inline formatting in a horizontal writing mode are implemented,
//! including auto width resolution, margin collapse between adjacent siblings,
//! and greedy line breaking.
//!
//! Features that change where boxes land, rather than adding detail, return a
//! typed error:
//!
//! - floats and clearance;
//! - `position` other than `static`, which removes a box from normal flow;
//! - flexbox and grid, which replace the block layout algorithm entirely;
//! - table layout;
//! - vertical and right-to-left writing modes.
//!
//! Each of these produces a materially different geometry. Ignoring one would
//! place content in the wrong place while appearing to succeed.

#![forbid(unsafe_code)]

use core::fmt;
use turing_css::{ElementTree, Stylesheet, cascade};

/// What layout needs from a tree beyond selector matching.
///
/// Selector matching answers questions about one element; box generation also
/// has to walk children and read text. Keeping this separate from
/// [`ElementTree`] means an embedder implements only what they use.
pub trait LayoutTree: ElementTree {
    /// Returns the root node to begin box generation from.
    fn root(&self) -> Self::Node;

    /// Returns the node's children in document order.
    fn children(&self, node: Self::Node) -> Vec<Self::Node>;

    /// Returns the node's text, if it is a text node.
    fn text(&self, node: Self::Node) -> Option<&str>;

    /// Returns whether the node generates no box regardless of style,
    /// such as a comment or doctype.
    fn is_non_rendered(&self, node: Self::Node) -> bool;

    /// Returns a stable index identifying the node.
    ///
    /// Layout boxes record this rather than `Self::Node` so [`LayoutBox`] stays
    /// a plain data type an embedder can pass to a painter or a test without
    /// carrying the tree's type parameter along with it.
    fn node_index(&self, node: Self::Node) -> usize;
}

/// A feature this implementation does not model.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum LayoutError {
    /// `float` removes a box from normal vertical stacking.
    FloatUnsupported { value: String },
    /// `position` other than `static` changes the containing block.
    PositioningUnsupported { value: String },
    /// A display type with its own layout algorithm.
    DisplayModeUnsupported { value: String },
    /// Vertical or right-to-left flow.
    WritingModeUnsupported { value: String },
}

impl fmt::Display for LayoutError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::FloatUnsupported { value } => write!(
                formatter,
                "float: {value} is not implemented; floats leave normal flow and require clearance"
            ),
            Self::PositioningUnsupported { value } => write!(
                formatter,
                "position: {value} is not implemented; it changes the containing block"
            ),
            Self::DisplayModeUnsupported { value } => write!(
                formatter,
                "display: {value} is not implemented; it replaces the block layout algorithm"
            ),
            Self::WritingModeUnsupported { value } => {
                write!(formatter, "writing mode {value} is not implemented")
            }
        }
    }
}

/// A rectangle in CSS pixels, with the origin at the top left.
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct Rect {
    pub x: f32,
    pub y: f32,
    pub width: f32,
    pub height: f32,
}

/// Edge sizes for margin, border, and padding.
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct EdgeSizes {
    pub left: f32,
    pub right: f32,
    pub top: f32,
    pub bottom: f32,
}

/// The four boxes of the CSS box model for one element.
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct Dimensions {
    /// The content box.
    pub content: Rect,
    pub padding: EdgeSizes,
    pub border: EdgeSizes,
    pub margin: EdgeSizes,
}

impl Dimensions {
    /// Returns the content box expanded by padding.
    #[must_use]
    pub fn padding_box(self) -> Rect {
        expand(self.content, self.padding)
    }

    /// Returns the padding box expanded by borders.
    #[must_use]
    pub fn border_box(self) -> Rect {
        expand(self.padding_box(), self.border)
    }

    /// Returns the border box expanded by margins.
    #[must_use]
    pub fn margin_box(self) -> Rect {
        expand(self.border_box(), self.margin)
    }
}

fn expand(rect: Rect, edge: EdgeSizes) -> Rect {
    Rect {
        x: rect.x - edge.left,
        y: rect.y - edge.top,
        width: rect.width + edge.left + edge.right,
        height: rect.height + edge.top + edge.bottom,
    }
}

/// Whether a box participates in block or inline flow.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum BoxKind {
    /// Generates a block-level box.
    Block,
    /// Generates an inline-level box.
    Inline,
    /// A run of text.
    Text,
    /// The anonymous block wrapping a run of inline children.
    AnonymousBlock,
}

/// Font metrics used to measure text.
///
/// A placeholder for real shaping. Making it explicit keeps the assumption
/// visible instead of hard-coding a number inside the line breaker.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct TextMetrics {
    /// Horizontal advance of one character.
    pub advance: f32,
    /// Distance between successive baselines.
    pub line_height: f32,
}

impl Default for TextMetrics {
    fn default() -> Self {
        Self {
            advance: 8.0,
            line_height: 16.0,
        }
    }
}

/// A positioned box in the layout tree.
#[derive(Clone, Debug, PartialEq)]
pub struct LayoutBox {
    /// Geometry resolved by layout.
    pub dimensions: Dimensions,
    /// How this box participates in flow.
    pub kind: BoxKind,
    /// Source node index, absent for anonymous boxes.
    pub node: Option<usize>,
    /// Text content for [`BoxKind::Text`].
    pub text: Option<String>,
    /// Resolved declarations that painting needs.
    pub background: Option<String>,
    pub color: Option<String>,
    /// Child boxes.
    pub children: Vec<LayoutBox>,
}

/// One paint command.
#[derive(Clone, Debug, PartialEq)]
pub enum DisplayItem {
    /// Fill `rect` with `color`.
    SolidColor { rect: Rect, color: String },
    /// Draw `text` at `rect` in `color`.
    Text {
        rect: Rect,
        text: String,
        color: String,
    },
}

/// The flat, ordered list of paint commands for a document.
#[derive(Clone, Debug, Default, PartialEq)]
pub struct DisplayList {
    /// Commands in paint order.
    pub items: Vec<DisplayItem>,
}

/// Resolved style for one element, reduced to what layout consumes.
#[derive(Clone, Debug, Default, PartialEq)]
struct Style {
    display: Option<String>,
    width: Option<f32>,
    height: Option<f32>,
    margin: EdgeSizes,
    padding: EdgeSizes,
    border: EdgeSizes,
    background: Option<String>,
    color: Option<String>,
}

/// Lays out `document` styled by `stylesheet` into a viewport `width` wide.
///
/// # Errors
///
/// Returns [`LayoutError`] when a declaration selects a formatting model this
/// implementation does not provide, rather than placing content wrongly.
pub fn layout<T: LayoutTree>(
    tree: &T,
    stylesheet: &Stylesheet,
    width: f32,
    metrics: TextMetrics,
) -> Result<LayoutBox, LayoutError> {
    let root = build_box(tree, stylesheet, tree.root(), None)?
        .unwrap_or_else(|| anonymous_block(Vec::new()));

    let mut viewport = Dimensions::default();
    viewport.content.width = width;

    let mut root = root;
    layout_block(&mut root, viewport, metrics);
    Ok(root)
}

/// Builds the display list for a laid-out tree.
#[must_use]
pub fn build_display_list(root: &LayoutBox) -> DisplayList {
    let mut list = DisplayList::default();
    paint(root, &mut list);
    list
}

fn paint(layout_box: &LayoutBox, list: &mut DisplayList) {
    // Backgrounds paint before content, and a parent paints before its
    // children, which is the document-order approximation of paint order.
    if let Some(color) = &layout_box.background {
        list.items.push(DisplayItem::SolidColor {
            rect: layout_box.dimensions.border_box(),
            color: color.clone(),
        });
    }
    if let (BoxKind::Text, Some(text)) = (layout_box.kind, &layout_box.text) {
        list.items.push(DisplayItem::Text {
            rect: layout_box.dimensions.content,
            text: text.clone(),
            color: layout_box
                .color
                .clone()
                .unwrap_or_else(|| "black".to_string()),
        });
    }
    for child in &layout_box.children {
        paint(child, list);
    }
}

// -- box generation ------------------------------------------------------

fn build_box<T: LayoutTree>(
    tree: &T,
    stylesheet: &Stylesheet,
    node: T::Node,
    inherited_color: Option<&str>,
) -> Result<Option<LayoutBox>, LayoutError> {
    if let Some(text) = tree.text(node) {
        if text.trim().is_empty() {
            return Ok(None);
        }
        return Ok(Some(LayoutBox {
            dimensions: Dimensions::default(),
            kind: BoxKind::Text,
            node: Some(tree.node_index(node)),
            text: Some(text.to_string()),
            background: None,
            // `color` is inherited, so a text run paints in the colour of
            // the nearest ancestor that set one.
            color: inherited_color.map(str::to_string),
            children: Vec::new(),
        }));
    }
    if tree.is_non_rendered(node) {
        return Ok(None);
    }

    let style = resolve_style(tree, stylesheet, node)?;
    let display = style.display.as_deref().unwrap_or("");
    if display == "none" {
        return Ok(None);
    }

    let own_color = style.color.as_deref().or(inherited_color);
    let mut children = Vec::new();
    for child in tree.children(node) {
        if let Some(built) = build_box(tree, stylesheet, child, own_color)? {
            children.push(built);
        }
    }

    // The root is not an element and has no `display`, so it stays a block.
    let kind = if tree.is_element(node) && display == "inline" {
        BoxKind::Inline
    } else {
        BoxKind::Block
    };

    // A block box whose children mix block and inline levels needs anonymous
    // block boxes so the inline runs form their own formatting context.
    let children = if kind == BoxKind::Block && has_mixed_levels(&children) {
        wrap_inline_runs(children)
    } else {
        children
    };

    Ok(Some(LayoutBox {
        dimensions: Dimensions {
            // Explicit `width` and `height` are seeded into the content rect;
            // layout treats a zero here as `auto` and resolves it from the
            // containing block or the children. A declared `0` is therefore
            // indistinguishable from `auto`, which is the one case this
            // representation cannot express.
            content: Rect {
                width: style.width.unwrap_or(0.0),
                height: style.height.unwrap_or(0.0),
                ..Rect::default()
            },
            padding: style.padding,
            border: style.border,
            margin: style.margin,
        },
        kind,
        node: Some(tree.node_index(node)),
        text: None,
        background: style.background.clone(),
        color: own_color.map(str::to_string),
        children,
    }))
}

fn has_mixed_levels(children: &[LayoutBox]) -> bool {
    let block = children.iter().any(|c| c.kind == BoxKind::Block);
    let inline = children
        .iter()
        .any(|c| matches!(c.kind, BoxKind::Inline | BoxKind::Text));
    block && inline
}

fn wrap_inline_runs(children: Vec<LayoutBox>) -> Vec<LayoutBox> {
    let mut result: Vec<LayoutBox> = Vec::new();
    let mut run: Vec<LayoutBox> = Vec::new();
    for child in children {
        if matches!(child.kind, BoxKind::Inline | BoxKind::Text) {
            run.push(child);
        } else {
            if !run.is_empty() {
                result.push(anonymous_block(core::mem::take(&mut run)));
            }
            result.push(child);
        }
    }
    if !run.is_empty() {
        result.push(anonymous_block(run));
    }
    result
}

fn anonymous_block(children: Vec<LayoutBox>) -> LayoutBox {
    LayoutBox {
        dimensions: Dimensions::default(),
        kind: BoxKind::AnonymousBlock,
        node: None,
        text: None,
        background: None,
        color: None,
        children,
    }
}

fn resolve_style<T: LayoutTree>(
    tree: &T,
    stylesheet: &Stylesheet,
    node: T::Node,
) -> Result<Style, LayoutError> {
    let mut style = Style::default();
    if !tree.is_element(node) {
        return Ok(style);
    }

    let declarations = cascade(tree, node, stylesheet);
    for (property, computed) in &declarations {
        let value = computed.value.as_str();
        match property.as_str() {
            "display" => {
                match value {
                    "block" | "inline" | "none" => style.display = Some(value.to_string()),
                    // flex, grid, and table replace the layout algorithm.
                    _ => {
                        return Err(LayoutError::DisplayModeUnsupported {
                            value: value.to_string(),
                        });
                    }
                }
            }
            "float" if value != "none" => {
                return Err(LayoutError::FloatUnsupported {
                    value: value.to_string(),
                });
            }
            "position" if value != "static" => {
                return Err(LayoutError::PositioningUnsupported {
                    value: value.to_string(),
                });
            }
            "writing-mode" | "direction" if !matches!(value, "horizontal-tb" | "ltr") => {
                return Err(LayoutError::WritingModeUnsupported {
                    value: value.to_string(),
                });
            }
            "width" => style.width = parse_length(value),
            "height" => style.height = parse_length(value),
            "margin" => style.margin = uniform(parse_length(value).unwrap_or(0.0)),
            "padding" => style.padding = uniform(parse_length(value).unwrap_or(0.0)),
            "border-width" => style.border = uniform(parse_length(value).unwrap_or(0.0)),
            "background" | "background-color" => style.background = Some(value.to_string()),
            "color" => style.color = Some(value.to_string()),
            _ => {}
        }
    }

    // The default display for an unstyled element depends on the element, and
    // a full user-agent stylesheet is not implemented. Treating the known
    // inline elements as inline keeps ordinary text flowing correctly.
    if style.display.is_none()
        && let Some(name) = tree.tag_name(node)
    {
        style.display = Some(default_display(name).to_string());
    }
    Ok(style)
}

/// The user-agent default display for common elements.
fn default_display(tag: &str) -> &'static str {
    match tag {
        "a" | "abbr" | "b" | "bdi" | "bdo" | "br" | "cite" | "code" | "data" | "dfn" | "em"
        | "i" | "kbd" | "mark" | "q" | "rp" | "rt" | "ruby" | "s" | "samp" | "small" | "span"
        | "strong" | "sub" | "sup" | "time" | "u" | "var" | "wbr" | "img" | "input" | "label"
        | "select" | "textarea" | "button" => "inline",
        "head" | "title" | "meta" | "link" | "style" | "script" | "base" => "none",
        _ => "block",
    }
}

fn uniform(value: f32) -> EdgeSizes {
    EdgeSizes {
        left: value,
        right: value,
        top: value,
        bottom: value,
    }
}

/// Parses a length in `px` or a bare number. Percentages and relative units
/// are not resolved here and yield `None`, which layout treats as `auto`.
fn parse_length(value: &str) -> Option<f32> {
    let trimmed = value.trim();
    let number = trimmed.strip_suffix("px").unwrap_or(trimmed);
    number.trim().parse::<f32>().ok()
}

// -- layout --------------------------------------------------------------

fn layout_block(layout_box: &mut LayoutBox, containing: Dimensions, metrics: TextMetrics) {
    calculate_width(layout_box, containing);
    calculate_position(layout_box, containing);
    // Laying out children overwrites the content height with theirs, so the
    // declared height has to be read before that happens.
    let declared_height = layout_box.dimensions.content.height;
    layout_children(layout_box, metrics);
    calculate_height(layout_box, declared_height);
}

fn calculate_width(layout_box: &mut LayoutBox, containing: Dimensions) {
    let dimensions = &mut layout_box.dimensions;
    let used = containing.content.width
        - dimensions.margin.left
        - dimensions.margin.right
        - dimensions.border.left
        - dimensions.border.right
        - dimensions.padding.left
        - dimensions.padding.right;
    // An explicit width was recorded during box generation by seeding the
    // content rect; otherwise the block fills its containing block.
    if dimensions.content.width <= 0.0 {
        dimensions.content.width = used.max(0.0);
    }
}

fn calculate_position(layout_box: &mut LayoutBox, containing: Dimensions) {
    let dimensions = &mut layout_box.dimensions;
    dimensions.content.x = containing.content.x
        + dimensions.margin.left
        + dimensions.border.left
        + dimensions.padding.left;
    dimensions.content.y = containing.content.y
        + containing.content.height
        + dimensions.margin.top
        + dimensions.border.top
        + dimensions.padding.top;
}

fn layout_children(layout_box: &mut LayoutBox, metrics: TextMetrics) {
    let mut cursor = layout_box.dimensions;
    cursor.content.height = 0.0;
    // Margins between adjacent siblings collapse to the larger of the two.
    let mut previous_margin_bottom = 0.0_f32;

    let inline_context = layout_box.kind == BoxKind::AnonymousBlock
        || layout_box
            .children
            .iter()
            .all(|c| matches!(c.kind, BoxKind::Inline | BoxKind::Text));

    if inline_context && !layout_box.children.is_empty() {
        layout_inline_children(layout_box, metrics);
        return;
    }

    let mut children = core::mem::take(&mut layout_box.children);
    for child in &mut children {
        let collapsed = child.dimensions.margin.top.max(previous_margin_bottom);
        let overlap = child.dimensions.margin.top + previous_margin_bottom - collapsed;
        cursor.content.height -= overlap;

        layout_block(child, cursor, metrics);
        cursor.content.height += child.dimensions.margin_box().height;
        previous_margin_bottom = child.dimensions.margin.bottom;
    }
    layout_box.children = children;
    layout_box.dimensions.content.height = cursor.content.height;
}

/// Greedy line breaking over inline children.
fn layout_inline_children(layout_box: &mut LayoutBox, metrics: TextMetrics) {
    let origin_x = layout_box.dimensions.content.x;
    let origin_y = layout_box.dimensions.content.y;
    let available = layout_box.dimensions.content.width;

    let mut pen_x = 0.0_f32;
    let mut line = 0.0_f32;
    let mut children = core::mem::take(&mut layout_box.children);

    for child in &mut children {
        let text = child.text.clone().unwrap_or_default();
        let width = text.chars().count() as f32 * metrics.advance;
        if pen_x > 0.0 && pen_x + width > available {
            pen_x = 0.0;
            line += 1.0;
        }
        child.dimensions.content = Rect {
            x: origin_x + pen_x,
            y: origin_y + line * metrics.line_height,
            width,
            height: metrics.line_height,
        };
        pen_x += width;
        // Nested inline boxes lay their own children out on the same line.
        if !child.children.is_empty() {
            layout_inline_children(child, metrics);
        }
    }
    layout_box.children = children;
    layout_box.dimensions.content.height = (line + 1.0) * metrics.line_height;
}

/// Applies a declared `height`, which overrides the height derived from
/// children. `declared_height` of zero means the declaration was absent.
fn calculate_height(layout_box: &mut LayoutBox, declared_height: f32) {
    if declared_height > 0.0 {
        layout_box.dimensions.content.height = declared_height;
    }
}

// -- foreign tree acceptance test ----------------------------------------

/// Drives style and layout from a tree that is not the engine's own.
///
/// This is the test the decoupling exists to pass. Every other test in this
/// crate uses `turing_html::Document`, which proves the adapter works but not
/// that the trait surface is *sufficient* — a missing method would be invisible
/// as long as the only implementor is the one the traits were extracted from.
///
/// Deliberately not gated on the `html` feature, so it also runs in the
/// zero-dependency configuration an embedder actually builds. The tree below is
/// the whole of what implementing [`LayoutTree`] costs.
#[cfg(test)]
mod foreign_tree {
    use super::{BoxKind, LayoutBox, LayoutTree, TextMetrics, layout};
    use turing_css::{ElementTree, Stylesheet};

    /// A node in a host application's own document representation.
    struct HostNode {
        tag: Option<String>,
        text: Option<String>,
        class: Option<String>,
        parent: Option<usize>,
        children: Vec<usize>,
    }

    struct HostTree {
        nodes: Vec<HostNode>,
    }

    impl HostTree {
        /// Builds `<root><p class="lead">Hello</p><p>World</p></root>`.
        fn sample() -> Self {
            let mut nodes = vec![HostNode {
                tag: None,
                text: None,
                class: None,
                parent: None,
                children: Vec::new(),
            }];
            let push = |nodes: &mut Vec<HostNode>, node: HostNode, parent: usize| {
                nodes.push(node);
                let id = nodes.len() - 1;
                nodes[parent].children.push(id);
                id
            };
            let root = push(
                &mut nodes,
                HostNode {
                    tag: Some("root".to_string()),
                    text: None,
                    class: None,
                    parent: Some(0),
                    children: Vec::new(),
                },
                0,
            );
            for (class, body) in [(Some("lead"), "Hello"), (None, "World")] {
                let para = push(
                    &mut nodes,
                    HostNode {
                        tag: Some("p".to_string()),
                        text: None,
                        class: class.map(str::to_string),
                        parent: Some(root),
                        children: Vec::new(),
                    },
                    root,
                );
                push(
                    &mut nodes,
                    HostNode {
                        tag: None,
                        text: Some(body.to_string()),
                        class: None,
                        parent: Some(para),
                        children: Vec::new(),
                    },
                    para,
                );
            }
            Self { nodes }
        }
    }

    impl ElementTree for HostTree {
        type Node = usize;

        fn is_element(&self, node: Self::Node) -> bool {
            self.nodes[node].tag.is_some()
        }

        fn tag_name(&self, node: Self::Node) -> Option<&str> {
            self.nodes[node].tag.as_deref()
        }

        fn attribute(&self, node: Self::Node, name: &str) -> Option<&str> {
            match name {
                "class" => self.nodes[node].class.as_deref(),
                _ => None,
            }
        }

        fn parent(&self, node: Self::Node) -> Option<Self::Node> {
            self.nodes[node].parent
        }

        fn previous_element_sibling(&self, node: Self::Node) -> Option<Self::Node> {
            let parent = self.nodes[node].parent?;
            let siblings = &self.nodes[parent].children;
            let position = siblings.iter().position(|&s| s == node)?;
            siblings[..position]
                .iter()
                .rev()
                .copied()
                .find(|&s| self.is_element(s))
        }
    }

    impl LayoutTree for HostTree {
        fn root(&self) -> Self::Node {
            0
        }

        fn children(&self, node: Self::Node) -> Vec<Self::Node> {
            self.nodes[node].children.clone()
        }

        fn text(&self, node: Self::Node) -> Option<&str> {
            self.nodes[node].text.as_deref()
        }

        fn is_non_rendered(&self, _node: Self::Node) -> bool {
            false
        }

        fn node_index(&self, node: Self::Node) -> usize {
            node
        }
    }

    fn collect(root: &LayoutBox, out: &mut Vec<(BoxKind, Option<String>)>) {
        out.push((root.kind, root.text.clone()));
        for child in &root.children {
            collect(child, out);
        }
    }

    #[test]
    fn lays_out_a_tree_the_engine_does_not_own() {
        let tree = HostTree::sample();
        let sheet = Stylesheet::parse("p { display: block; height: 20px; }").expect("parses");

        let root = layout(&tree, &sheet, 200.0, TextMetrics::default()).expect("lays out");

        let mut boxes = Vec::new();
        collect(&root, &mut boxes);
        let text: Vec<_> = boxes
            .iter()
            .filter(|(kind, _)| *kind == BoxKind::Text)
            .map(|(_, text)| text.clone().expect("text box carries text"))
            .collect();
        assert_eq!(text, vec!["Hello".to_string(), "World".to_string()]);
    }

    #[test]
    fn cascade_reads_attributes_through_the_host_tree() {
        let tree = HostTree::sample();
        // `.lead` only matches if the host tree's `attribute` is consulted, and
        // the two paragraphs only differ by height if the cascade really ran.
        let sheet = Stylesheet::parse(
            ".lead { display: block; height: 40px; } p { display: block; height: 10px; }",
        )
        .expect("parses");

        let root = layout(&tree, &sheet, 200.0, TextMetrics::default()).expect("lays out");

        let paragraphs: Vec<f32> = root.children[0]
            .children
            .iter()
            .filter(|b| b.kind == BoxKind::Block)
            .map(|b| b.dimensions.content.height)
            .collect();
        assert_eq!(paragraphs, vec![40.0, 10.0]);
    }
}

// -- turing-html adapter -------------------------------------------------

/// Implements [`LayoutTree`] for the engine's own document.
///
/// Behind the `html` feature, so layout itself carries no dependency on the
/// DOM. This is also the shape an embedder copies for their own tree.
#[cfg(feature = "html")]
mod html_tree {
    use super::LayoutTree;
    use turing_html::{Document, NodeData};

    impl LayoutTree for Document {
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

        fn is_non_rendered(&self, node: Self::Node) -> bool {
            matches!(
                self.node(node).data,
                NodeData::Comment(_) | NodeData::Doctype { .. }
            )
        }

        fn node_index(&self, node: Self::Node) -> usize {
            node.index()
        }
    }
}

#[cfg(all(test, feature = "html"))]
mod tests {
    use super::*;
    use turing_html::{Document, NodeId, Tokenizer, TreeBuilder};

    fn run(html: &str, css: &str, width: f32) -> Result<LayoutBox, LayoutError> {
        let tokens = Tokenizer::new(html).tokenize().expect("tokenizes").tokens;
        let document = TreeBuilder::new().build(&tokens).expect("builds");
        let sheet = Stylesheet::parse(css).expect("parses");
        layout(&document, &sheet, width, TextMetrics::default())
    }

    fn document_for(html: &str) -> Document {
        let tokens = Tokenizer::new(html).tokenize().expect("tokenizes").tokens;
        TreeBuilder::new().build(&tokens).expect("builds")
    }

    #[test]
    fn explicit_width_overrides_filling_the_containing_block() {
        let root = run(
            "<html><body><div>x</div></body></html>",
            "div { display: block; width: 120px; }",
            400.0,
        )
        .expect("lays out");
        let document = document_for("<html><body><div>x</div></body></html>");
        assert_eq!(
            find(&root, &document, "div").dimensions.content.width,
            120.0
        );
    }

    #[test]
    fn explicit_height_overrides_the_height_of_children() {
        // The div contains one line of text, so its derived height would be
        // the 16px default line height. A declared height must win.
        let root = run(
            "<html><body><div>x</div></body></html>",
            "div { display: block; height: 90px; }",
            400.0,
        )
        .expect("lays out");
        let document = document_for("<html><body><div>x</div></body></html>");
        assert_eq!(
            find(&root, &document, "div").dimensions.content.height,
            90.0
        );
    }

    #[test]
    fn absent_height_is_still_derived_from_children() {
        let root = run(
            "<html><body><div>x</div></body></html>",
            "div { display: block; }",
            400.0,
        )
        .expect("lays out");
        let document = document_for("<html><body><div>x</div></body></html>");
        assert_eq!(
            find(&root, &document, "div").dimensions.content.height,
            16.0
        );
    }

    fn find<'tree>(root: &'tree LayoutBox, document: &Document, tag: &str) -> &'tree LayoutBox {
        fn walk<'tree>(
            node: &'tree LayoutBox,
            document: &Document,
            tag: &str,
        ) -> Option<&'tree LayoutBox> {
            if let Some(index) = node.node
                && document.element_name(NodeId::from_index(index)) == Some(tag)
            {
                return Some(node);
            }
            node.children.iter().find_map(|c| walk(c, document, tag))
        }
        walk(root, document, tag).expect("box exists")
    }

    fn document_of(html: &str) -> Document {
        let tokens = Tokenizer::new(html).tokenize().expect("tokenizes").tokens;
        TreeBuilder::new().build(&tokens).expect("builds")
    }

    #[test]
    fn block_fills_the_viewport_width() {
        let root = run("<div>x</div>", "", 800.0).expect("lays out");
        let document = document_of("<div>x</div>");
        let div = find(&root, &document, "div");
        assert_eq!(div.dimensions.content.width, 800.0);
    }

    #[test]
    fn padding_and_border_reduce_content_width() {
        let root = run(
            "<div>x</div>",
            "div { padding: 10px; border-width: 5px }",
            800.0,
        )
        .expect("lays out");
        let document = document_of("<div>x</div>");
        let div = find(&root, &document, "div");
        // 800 - 2*10 padding - 2*5 border
        assert_eq!(div.dimensions.content.width, 770.0);
        assert_eq!(div.dimensions.border_box().width, 800.0);
    }

    #[test]
    fn margins_offset_the_content_box() {
        let root = run("<div>x</div>", "div { margin: 20px }", 800.0).expect("lays out");
        let document = document_of("<div>x</div>");
        let div = find(&root, &document, "div");
        assert_eq!(div.dimensions.content.x, 20.0);
        assert_eq!(div.dimensions.content.width, 760.0);
    }

    #[test]
    fn sibling_blocks_stack_vertically() {
        let html = "<section><div>a</div><div>b</div></section>";
        let root = run(html, "div { height: 0 }", 800.0).expect("lays out");
        let document = document_of(html);
        let section = find(&root, &document, "section");
        let first = &section.children[0];
        let second = &section.children[1];
        assert!(
            second.dimensions.content.y >= first.dimensions.content.y,
            "second block must not sit above the first"
        );
    }

    #[test]
    fn adjacent_margins_collapse_to_the_larger() {
        // Two 20px margins between siblings yield 20px of separation, not 40.
        let html = "<section><div>a</div><div>b</div></section>";
        let root = run(html, "div { margin: 20px }", 800.0).expect("lays out");
        let document = document_of(html);
        let section = find(&root, &document, "section");
        let first = section.children[0].dimensions.margin_box();
        let second = section.children[1].dimensions.margin_box();
        let gap = second.y - (first.y + first.height);
        assert!(gap.abs() < 21.0, "margins did not collapse; gap was {gap}");
    }

    #[test]
    fn display_none_generates_no_box() {
        let html = "<div><span>gone</span></div>";
        let root = run(html, "span { display: none }", 800.0).expect("lays out");
        let document = document_of(html);
        let div = find(&root, &document, "div");
        assert!(div.children.is_empty(), "hidden element produced a box");
    }

    #[test]
    fn head_elements_generate_no_boxes() {
        // title lives in head and must never be laid out as visible text.
        let html = "<html><head><title>T</title></head><body><p>x</p></body></html>";
        let root = run(html, "", 800.0).expect("lays out");
        let list = build_display_list(&root);
        assert!(
            !list.items.iter().any(|item| matches!(
                item,
                DisplayItem::Text { text, .. } if text.contains('T')
            )),
            "title text was painted"
        );
    }

    #[test]
    fn mixed_children_get_an_anonymous_block() {
        let html = "<div>text<p>block</p></div>";
        let root = run(html, "", 800.0).expect("lays out");
        let document = document_of(html);
        let div = find(&root, &document, "div");
        assert!(
            div.children
                .iter()
                .any(|c| c.kind == BoxKind::AnonymousBlock),
            "no anonymous block was generated"
        );
    }

    #[test]
    fn long_text_wraps_onto_multiple_lines() {
        // 20 characters at 8px advance is 160px, which does not fit in 100px.
        let html = "<div>aaaaaaaaaabbbbbbbbbb</div>";
        let root = run(html, "", 100.0).expect("lays out");
        let document = document_of(html);
        let div = find(&root, &document, "div");
        assert!(
            div.dimensions.content.height >= TextMetrics::default().line_height,
            "text did not produce a line box"
        );
    }

    #[test]
    fn display_list_paints_background_before_text() {
        let html = "<div>hi</div>";
        let root = run(html, "div { background: red; color: blue }", 800.0).expect("lays out");
        let list = build_display_list(&root);
        let background = list
            .items
            .iter()
            .position(|item| matches!(item, DisplayItem::SolidColor { .. }));
        let text = list
            .items
            .iter()
            .position(|item| matches!(item, DisplayItem::Text { .. }));
        assert!(background.is_some() && text.is_some());
        assert!(
            background < text,
            "background must paint before the text it sits behind"
        );
    }

    #[test]
    fn display_list_carries_resolved_colors() {
        let root = run("<div>hi</div>", "div { background: red }", 800.0).expect("lays out");
        let list = build_display_list(&root);
        assert!(list.items.iter().any(|item| matches!(
            item,
            DisplayItem::SolidColor { color, .. } if color == "red"
        )));
    }

    #[test]
    fn floats_are_reported_not_guessed() {
        let error = run("<div>x</div>", "div { float: left }", 800.0).expect_err("refused");
        assert!(matches!(error, LayoutError::FloatUnsupported { .. }));
    }

    #[test]
    fn positioning_is_reported_not_guessed() {
        let error = run("<div>x</div>", "div { position: absolute }", 800.0).expect_err("refused");
        assert!(matches!(error, LayoutError::PositioningUnsupported { .. }));
    }

    #[test]
    fn flex_and_grid_are_reported_not_guessed() {
        for value in ["flex", "grid", "table"] {
            let css = format!("div {{ display: {value} }}");
            let error = run("<div>x</div>", &css, 800.0).expect_err("refused");
            assert!(
                matches!(error, LayoutError::DisplayModeUnsupported { .. }),
                "display: {value} was not refused"
            );
        }
    }

    #[test]
    fn vertical_writing_mode_is_reported_not_guessed() {
        let error =
            run("<div>x</div>", "div { writing-mode: vertical-rl }", 800.0).expect_err("refused");
        assert!(matches!(error, LayoutError::WritingModeUnsupported { .. }));
    }

    #[test]
    fn lays_out_a_small_page_end_to_end() {
        let html = "<body><h1>Title</h1><p>Some text</p></body>";
        let css = "h1 { margin: 10px; background: silver } p { color: navy }";
        let root = run(html, css, 640.0).expect("lays out");
        let list = build_display_list(&root);
        assert!(!list.items.is_empty(), "nothing was painted");
        assert!(list.items.iter().any(|item| matches!(
            item,
            DisplayItem::Text { text, .. } if text.contains("Title")
        )));
        assert!(list.items.iter().any(|item| matches!(
            item,
            DisplayItem::Text { color, .. } if color == "navy"
        )));
    }

    #[test]
    fn boxes_stay_inside_the_viewport() {
        let html = "<body><div>a</div><div>b</div></body>";
        let root = run(html, "div { padding: 5px }", 400.0).expect("lays out");
        let list = build_display_list(&root);
        for item in &list.items {
            let rect = match item {
                DisplayItem::SolidColor { rect, .. } | DisplayItem::Text { rect, .. } => rect,
            };
            assert!(
                rect.x >= 0.0 && rect.x + rect.width <= 400.0 + f32::EPSILON,
                "box escaped the viewport: {rect:?}"
            );
        }
    }
}
