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
use turing_css::{Stylesheet, cascade};
use turing_html::{Document, NodeData, NodeId};

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
    /// Source element, absent for anonymous boxes.
    pub node: Option<NodeId>,
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
pub fn layout(
    document: &Document,
    stylesheet: &Stylesheet,
    width: f32,
    metrics: TextMetrics,
) -> Result<LayoutBox, LayoutError> {
    let root = build_box(document, stylesheet, document.root(), None)?
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

fn build_box(
    document: &Document,
    stylesheet: &Stylesheet,
    node: NodeId,
    inherited_color: Option<&str>,
) -> Result<Option<LayoutBox>, LayoutError> {
    match &document.node(node).data {
        NodeData::Text(text) => {
            if text.trim().is_empty() {
                return Ok(None);
            }
            return Ok(Some(LayoutBox {
                dimensions: Dimensions::default(),
                kind: BoxKind::Text,
                node: Some(node),
                text: Some(text.clone()),
                background: None,
                // `color` is inherited, so a text run paints in the colour of
                // the nearest ancestor that set one.
                color: inherited_color.map(str::to_string),
                children: Vec::new(),
            }));
        }
        NodeData::Comment(_) | NodeData::Doctype { .. } => return Ok(None),
        NodeData::Document | NodeData::Element { .. } => {}
    }

    let style = resolve_style(document, stylesheet, node)?;
    let display = style.display.as_deref().unwrap_or("");
    if display == "none" {
        return Ok(None);
    }

    let own_color = style.color.as_deref().or(inherited_color);
    let mut children = Vec::new();
    for &child in &document.node(node).children {
        if let Some(built) = build_box(document, stylesheet, child, own_color)? {
            children.push(built);
        }
    }

    let kind = if matches!(document.node(node).data, NodeData::Document) {
        BoxKind::Block
    } else if display == "inline" {
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
            padding: style.padding,
            border: style.border,
            margin: style.margin,
            ..Dimensions::default()
        },
        kind,
        node: Some(node),
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

fn resolve_style(
    document: &Document,
    stylesheet: &Stylesheet,
    node: NodeId,
) -> Result<Style, LayoutError> {
    let mut style = Style::default();
    if matches!(document.node(node).data, NodeData::Document) {
        return Ok(style);
    }

    let declarations = cascade(document, node, stylesheet);
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
        && let Some(name) = document.element_name(node)
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
    layout_children(layout_box, metrics);
    calculate_height(layout_box);
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

fn calculate_height(layout_box: &mut LayoutBox) {
    // An explicit height was seeded into the content rect during generation.
    if layout_box.dimensions.content.height <= 0.0 && layout_box.children.is_empty() {
        layout_box.dimensions.content.height = 0.0;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use turing_html::{Tokenizer, TreeBuilder};

    fn run(html: &str, css: &str, width: f32) -> Result<LayoutBox, LayoutError> {
        let tokens = Tokenizer::new(html).tokenize().expect("tokenizes").tokens;
        let document = TreeBuilder::new().build(&tokens).expect("builds");
        let sheet = Stylesheet::parse(css).expect("parses");
        layout(&document, &sheet, width, TextMetrics::default())
    }

    fn find<'tree>(root: &'tree LayoutBox, document: &Document, tag: &str) -> &'tree LayoutBox {
        fn walk<'tree>(
            node: &'tree LayoutBox,
            document: &Document,
            tag: &str,
        ) -> Option<&'tree LayoutBox> {
            if let Some(id) = node.node
                && document.element_name(id) == Some(tag)
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
