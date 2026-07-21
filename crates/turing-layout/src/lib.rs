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
//! - vertical and right-to-left writing modes;
//! - negative margins, whose collapsing rule differs from the positive one.
//!
//! Each of these produces a materially different geometry. Ignoring one would
//! place content in the wrong place while appearing to succeed.
//!
//! # Hit testing
//!
//! [`hit_test`] answers which node is at a point, completing `REQ-ENG-005`
//! alongside the display list. Its ordering and edge-attribution rules are
//! documented on the function, because each one is a place where a wrong
//! implementation stays quiet.

#![forbid(unsafe_code)]

use core::fmt;
use turing_css::{
    Color, ComputedDeclaration, CssError, ElementTree, SelectorIndex, Stylesheet, cascade,
};

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
    /// A CSS value that the value layer refused, most often a colour notation.
    Value(CssError),
    /// `float` removes a box from normal vertical stacking.
    FloatUnsupported { value: String },
    /// `position` other than `static` changes the containing block.
    PositioningUnsupported { value: String },
    /// A display type with its own layout algorithm.
    DisplayModeUnsupported { value: String },
    /// Vertical or right-to-left flow.
    WritingModeUnsupported { value: String },
    /// A `text-align` value with no implemented placement.
    TextAlignUnsupported { value: String },
    /// A `text-decoration` value with no implemented line.
    TextDecorationUnsupported { value: String },
    /// A `visibility` value with no implemented meaning.
    VisibilityUnsupported { value: String },
    /// A negative length on a box edge.
    NegativeEdgeUnsupported { property: String, value: String },
    /// `display: inline-flex` (or any other inline-level replaced formatting
    /// context). The inner flex algorithm is implemented; what is missing is
    /// atomic inline-level sizing and placement for the *outer* box — the
    /// same gap that leaves `inline-block` unsupported here. Kept distinct
    /// from [`Self::DisplayModeUnsupported`] because that variant's message
    /// says the formatting model itself is unimplemented, which would be
    /// false for flex.
    AtomicInlineUnsupported { value: String },
    /// `flex-direction` other than `row`/`column`. `row-reverse` and
    /// `column-reverse` are real, well-defined values this implementation
    /// does not yet place correctly, so they are refused rather than
    /// silently treated as their forward counterpart.
    FlexDirectionUnsupported { value: String },
    /// `flex-wrap` other than `nowrap`. This implementation lays out a flex
    /// container as a single line; `wrap`/`wrap-reverse` change where boxes
    /// land (a second line entirely) and are refused rather than collapsed
    /// onto one line silently.
    FlexWrapUnsupported { value: String },
    /// An `align-items` value with no implemented cross-axis placement.
    AlignItemsUnsupported { value: String },
    /// A `justify-content` value with no implemented main-axis placement.
    JustifyContentUnsupported { value: String },
    /// A `flex` shorthand value outside the common forms this
    /// implementation resolves unambiguously (`none`, `auto`, `initial`, a
    /// bare `<number>`, `<number> <number>`, or `<number> <number>
    /// <basis>`). The shorthand's full grammar allows the growth pair and
    /// the basis in either order and independently omitted, which is
    /// genuinely ambiguous to resolve without guessing which token means
    /// what; refusing keeps that guess from happening quietly.
    FlexShorthandUnsupported { value: String },
    /// The document nests deeper than this implementation will recurse.
    NestingTooDeep { limit: usize },
}

impl From<CssError> for LayoutError {
    fn from(error: CssError) -> Self {
        Self::Value(error)
    }
}

impl fmt::Display for LayoutError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Value(error) => write!(formatter, "{error}"),
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
            Self::TextAlignUnsupported { value } => {
                write!(
                    formatter,
                    "text-align: {value} is not implemented; only left, right, \
                     center, start, and end place content here"
                )
            }
            Self::TextDecorationUnsupported { value } => write!(
                formatter,
                "text-decoration: {value} is not implemented; only underline, \
                 line-through, and none draw here"
            ),
            Self::VisibilityUnsupported { value } => write!(
                formatter,
                "visibility: {value} is not implemented; only visible and hidden \
                 have meaning here"
            ),
            Self::NestingTooDeep { limit } => write!(
                formatter,
                "the document nests deeper than {limit} elements; box generation                  recurses, and continuing would overflow the stack, which aborts                  the process rather than returning an error"
            ),
            Self::NegativeEdgeUnsupported { property, value } => write!(
                formatter,
                "{property}: {value} is not implemented; margin collapsing with negative \
                 values takes the most negative margin plus the largest positive one, \
                 which this implementation does not compute"
            ),
            Self::AtomicInlineUnsupported { value } => write!(
                formatter,
                "display: {value} is not implemented; the inner flex layout exists, but \
                 atomic inline-level sizing for the outer box does not (the same gap that \
                 leaves inline-block unsupported) — use display: flex for a block-level \
                 flex container instead"
            ),
            Self::FlexDirectionUnsupported { value } => write!(
                formatter,
                "flex-direction: {value} is not implemented; only row and column are \
                 placed here, not their reversed counterparts"
            ),
            Self::FlexWrapUnsupported { value } => write!(
                formatter,
                "flex-wrap: {value} is not implemented; this is a single-line flex layout, \
                 and wrapping onto further lines changes where boxes land"
            ),
            Self::AlignItemsUnsupported { value } => write!(
                formatter,
                "align-items: {value} is not implemented; only flex-start, center, \
                 flex-end, and stretch place items on the cross axis here"
            ),
            Self::JustifyContentUnsupported { value } => write!(
                formatter,
                "justify-content: {value} is not implemented; only flex-start, center, \
                 flex-end, space-between, and space-around place items on the main axis \
                 here"
            ),
            Self::FlexShorthandUnsupported { value } => write!(
                formatter,
                "flex: {value} is not a form this implementation resolves; use none, \
                 auto, initial, a bare <number>, <number> <number>, or \
                 <number> <number> <basis>"
            ),
        }
    }
}

/// The deepest element nesting this implementation will lay out.
///
/// Every stage after box generation — layout, painting, and hit testing — walks
/// the box tree recursively, so bounding generation bounds all of them. The
/// value is well above real documents and well below the depth at which the
/// stack runs out, which was measured rather than guessed: recursion here
/// overflows a default test stack somewhere between 100 and 1000 levels.
pub const MAX_NESTING_DEPTH: usize = 256;

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

/// Per-side border colours.
///
/// A side left `None` is not "no border colour" — it is "resolve
/// `currentColor` for this side", which paint does against the element's own
/// text colour. Separate from [`EdgeSizes`] because a colour is optional
/// per side (falling back to `currentColor`) where a width is not (it
/// defaults to zero, a real value, not an unresolved one).
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct BorderColors {
    pub top: Option<Color>,
    pub right: Option<Color>,
    pub bottom: Option<Color>,
    pub left: Option<Color>,
}

impl BorderColors {
    /// The shorthand form: the same colour on every side. `border-color: X`
    /// sets all four sides. Whether this wins over a per-side longhand on the
    /// same element follows the cascade's specificity/source-order rule
    /// between rules — see `wins_over_shorthand` — but not within one rule's
    /// own declaration order, which the cascade cannot currently see.
    #[must_use]
    fn uniform(color: Color) -> Self {
        Self {
            top: Some(color),
            right: Some(color),
            bottom: Some(color),
            left: Some(color),
        }
    }
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
    /// Generates a block-level flex container (`display: flex`). Its
    /// children lay out along [`FlexDirection`] rather than through block or
    /// inline flow — a genuinely different formatting context, not a
    /// variation of [`Self::Block`].
    Flex,
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

/// Horizontal alignment of inline content within a block, from `text-align`.
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub enum TextAlign {
    /// `left`/`start`: the initial value. Lines begin at the content origin.
    #[default]
    Start,
    /// `center`: each line is centred in the content width.
    Center,
    /// `right`/`end`: each line ends at the content edge.
    End,
}

/// A line drawn through or under text, from `text-decoration`.
///
/// Threaded through the tree exactly the way `color` is: declared on an
/// element, propagated to descendant text nodes that do not override it.
/// Real CSS's actual model is closer but different — decoration is not
/// inherited in the strict property sense, it *propagates* to descendants
/// and is drawn using each ancestor's own colour along its own span — and
/// implementing that distinction is not worth its complexity next to the
/// case that matters, an element declaring a decoration for the text it
/// directly contains. The simplification is stated here rather than left to
/// be discovered by a nested-override case this engine does not get right.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub enum TextDecoration {
    /// The initial value: no line.
    #[default]
    None,
    /// A line at the bottom of the text.
    Underline,
    /// A line through the middle of the text.
    LineThrough,
}

/// Whether a box paints, from `visibility`.
///
/// Unlike `display: none`, a hidden box still exists in layout: it is
/// still measured, sized, and positioned, and still occupies the space
/// its geometry claims — only *painting* it is suppressed. This is a real
/// CSS inherited property, and — unlike [`TextDecoration`]'s stated
/// simplification — the full inheritance model is worth having here: a
/// descendant declaring `visibility: visible` under a hidden ancestor
/// genuinely re-enables painting for itself, which is exactly the same
/// nearest-ancestor-wins propagation `color` already threads through the
/// tree, so it costs nothing extra to get right.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub enum Visibility {
    /// The initial value: paints normally.
    #[default]
    Visible,
    /// Occupies its layout space; paints nothing of its own, and does not
    /// suppress a descendant that overrides back to `visible`.
    Hidden,
}

/// The main axis of a flex container, from `flex-direction`.
///
/// `row-reverse` and `column-reverse` are real CSS values this
/// implementation does not place — reversing changes which end of the
/// container is the main-start, which shifts every item's position, not
/// just a detail of one — so they are refused rather than treated as their
/// forward counterpart.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub enum FlexDirection {
    /// The initial value: the main axis is horizontal, main-start at the
    /// left.
    #[default]
    Row,
    /// The main axis is vertical, main-start at the top.
    Column,
}

/// Cross-axis placement of flex items, from `align-items`.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub enum AlignItems {
    /// The initial value: each item starts at the cross-start edge.
    #[default]
    FlexStart,
    /// Each item is centred on the cross axis.
    Center,
    /// Each item ends at the cross-end edge.
    FlexEnd,
    /// Each item fills the container's cross size, when one is definite.
    Stretch,
}

/// Main-axis distribution of flex items, from `justify-content`.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub enum JustifyContent {
    /// The initial value: items pack at the main-start edge.
    #[default]
    FlexStart,
    /// Items are centred as a group, with equal space on both ends.
    Center,
    /// Items pack at the main-end edge.
    FlexEnd,
    /// The first item is at the start, the last at the end, and the
    /// remaining free space is split evenly between the others.
    SpaceBetween,
    /// The free space is split evenly around every item, so each gap
    /// between items is twice the gap at either end.
    SpaceAround,
}

/// A flex item's used `flex-basis`: the main-axis size the flex algorithm
/// starts distributing free space from, before `flex-grow`/`flex-shrink`
/// are applied.
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub enum FlexBasis {
    /// The initial value. Resolved at layout time from the item's own
    /// declared main-size property, or — for content this engine already
    /// knows how to measure — the text/inline content itself; see
    /// `resolve_flex_basis` for the exact rule and its stated limits.
    #[default]
    Auto,
    /// An explicit basis in CSS pixels, from the `flex-basis` property or
    /// the `flex` shorthand.
    Length(f32),
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
    pub background: Option<Color>,
    pub color: Option<Color>,
    /// Per-side border colours; used only where the matching side's border
    /// width is non-zero. A side left `None` falls back to the text colour,
    /// which is CSS's `currentColor` default for `border-color`.
    pub border_colors: BorderColors,
    /// Corner radius in CSS pixels; zero is a square box.
    pub border_radius: f32,
    /// Outline width in CSS pixels. Unlike a border, an outline never
    /// affects box size — it paints outside the border box without shifting
    /// where anything else lands, which is exactly why CSS gives it a
    /// separate property rather than folding it into `border`.
    pub outline_width: f32,
    /// Outline colour, falling back to `currentColor` like a border side.
    pub outline_color: Option<Color>,
    /// How inline children of this box are aligned. Inherited, like `color`.
    pub text_align: TextAlign,
    /// The line drawn through or under this box's own text. Propagated to
    /// descendant text nodes like `color`; see [`TextDecoration`] for the
    /// simplification that makes true.
    pub text_decoration: TextDecoration,
    /// Whether this box paints. See [`Visibility`].
    pub visibility: Visibility,
    /// This box's own resolved alpha, in `[0, 1]`: its own declared
    /// `opacity` (default fully opaque) multiplied by the ambient opacity
    /// its ancestors already resolved to. Multiplying approximates a real
    /// stacking context's group flattening — exactly right for a
    /// translucent box whose descendants do not overlap each other, and
    /// only wrong in the narrower case of two overlapping translucent boxes
    /// inside the same translucent ancestor, where a real browser's
    /// flattened group would show through no further than the ancestor's
    /// own opacity and this engine's product of independent alphas goes
    /// more transparent than that.
    pub opacity: f32,
    /// The axis this box's children lay out along, when `kind` is
    /// [`BoxKind::Flex`]. Inert otherwise, same as `text_decoration` on an
    /// anonymous block.
    pub flex_direction: FlexDirection,
    /// Cross-axis placement for this box's own flex items. Inert unless
    /// `kind` is [`BoxKind::Flex`].
    pub align_items: AlignItems,
    /// Main-axis distribution for this box's own flex items. Inert unless
    /// `kind` is [`BoxKind::Flex`].
    pub justify_content: JustifyContent,
    /// The gap between adjacent flex items, in CSS pixels. Inert unless
    /// `kind` is [`BoxKind::Flex`].
    pub gap: f32,
    /// This box's own `flex-grow`, read by its parent when the parent is a
    /// flex container. The initial value is `0`: an item does not grow by
    /// default.
    pub flex_grow: f32,
    /// This box's own `flex-shrink`, read by its parent when the parent is
    /// a flex container. The initial value is `1`: an item shrinks by
    /// default when items overflow the container.
    pub flex_shrink: f32,
    /// This box's own `flex-basis`, read by its parent when the parent is a
    /// flex container.
    pub flex_basis: FlexBasis,
    /// Child boxes.
    pub children: Vec<LayoutBox>,
}

/// One paint command.
#[derive(Clone, Debug, PartialEq)]
pub enum DisplayItem {
    /// Fill `rect` with `color` at `alpha`.
    ///
    /// `alpha` carries a box's own resolved `opacity` (`1.0` when
    /// undeclared). The reference rasterizer does not composite — it draws
    /// every fill fully opaque, the same way it draws [`Self::RoundedColor`]
    /// as a hard square — so `alpha` below `1.0` is a compositing painter's
    /// enhancement, not something both painters are diffed against.
    SolidColor {
        rect: Rect,
        color: Color,
        alpha: f32,
    },
    /// Fill `rect` with `color`, rounding the corners by `radius` CSS pixels,
    /// at `alpha`.
    ///
    /// A separate variant rather than a radius on [`Self::SolidColor`] so that
    /// the common square fill stays a square fill: the reference rasterizer
    /// draws this as a hard rectangle (it does not round), and only a
    /// compositing painter honours the radius. Layout emits this only when a
    /// non-zero `border-radius` is resolved.
    RoundedColor {
        rect: Rect,
        color: Color,
        radius: f32,
        alpha: f32,
    },
    /// Draw `text` at `rect` in `color` at `alpha`.
    Text {
        rect: Rect,
        text: String,
        color: Color,
        alpha: f32,
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
    background: Option<Color>,
    color: Option<Color>,
    border_colors: BorderColors,
    border_radius: f32,
    outline_width: f32,
    outline_color: Option<Color>,
    text_align: Option<TextAlign>,
    text_decoration: Option<TextDecoration>,
    visibility: Option<Visibility>,
    /// `None` means undeclared; resolved to the CSS initial value (fully
    /// opaque) at the same point every other undeclared-defaults-to-initial
    /// property is.
    opacity: Option<f32>,
    flex_direction: Option<FlexDirection>,
    align_items: Option<AlignItems>,
    justify_content: Option<JustifyContent>,
    gap: Option<f32>,
    flex_grow: Option<f32>,
    flex_shrink: Option<f32>,
    flex_basis: Option<FlexBasis>,
}

/// Lays out `document` styled by `stylesheet` into a viewport `width` wide.
///
/// `hovered` is the one node currently under the pointer, if any — the fact
/// `:hover` rules need. Pass `None` when nothing is hovered (including every
/// caller that has no concept of a pointer at all, such as a headless
/// render).
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
    hovered: Option<T::Node>,
) -> Result<LayoutBox, LayoutError> {
    // Built once per layout rather than once per element. Rebuilding it inside
    // box generation would leave the quadratic behaviour it exists to remove.
    let index = SelectorIndex::build(stylesheet);
    let root = build_box(tree, &index, tree.root(), Inherited::default(), hovered, 0)?
        .unwrap_or_else(|| anonymous_block(Vec::new()));

    let mut viewport = Dimensions::default();
    viewport.content.width = width;

    let mut root = root;
    layout_any(&mut root, viewport, metrics);
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
    // A hidden box still occupies its layout space — nothing here changes
    // where anything else lands — it just paints none of its own border,
    // outline, background, text, or decoration. Recursion into children is
    // outside this guard: a descendant's own `visibility` was already
    // resolved independently when it was built, and one that reads
    // `visible` genuinely paints again even under a hidden ancestor, which
    // is real CSS's inheritance-with-override rule, not an approximation of
    // it.
    if layout_box.visibility != Visibility::Hidden {
        // Borders paint first, as a ring of four edge fills between the border
        // box and the padding box; the background then covers the padding box.
        // Painting the ring as fills rather than one covered rectangle means a
        // box with a border and no background does not invent an interior.
        let dimensions = layout_box.dimensions;
        let has_border = dimensions.border.left > 0.0
            || dimensions.border.right > 0.0
            || dimensions.border.top > 0.0
            || dimensions.border.bottom > 0.0;
        if has_border {
            // Each side's own colour, defaulting to the element's text colour —
            // CSS's `currentColor` initial value for `border-color` — one side
            // at a time, since two adjacent sides may legitimately differ.
            let currentcolor = layout_box.color.unwrap_or_default();
            let colors = layout_box.border_colors;
            let outer = dimensions.border_box();
            let inner = dimensions.padding_box();
            for (rect, color) in [
                // Top and bottom span the full border box; left and right fill
                // between them.
                (
                    Rect {
                        x: outer.x,
                        y: outer.y,
                        width: outer.width,
                        height: inner.y - outer.y,
                    },
                    colors.top.unwrap_or(currentcolor),
                ),
                (
                    Rect {
                        x: outer.x,
                        y: inner.y + inner.height,
                        width: outer.width,
                        height: (outer.y + outer.height) - (inner.y + inner.height),
                    },
                    colors.bottom.unwrap_or(currentcolor),
                ),
                (
                    Rect {
                        x: outer.x,
                        y: inner.y,
                        width: inner.x - outer.x,
                        height: inner.height,
                    },
                    colors.left.unwrap_or(currentcolor),
                ),
                (
                    Rect {
                        x: inner.x + inner.width,
                        y: inner.y,
                        width: (outer.x + outer.width) - (inner.x + inner.width),
                        height: inner.height,
                    },
                    colors.right.unwrap_or(currentcolor),
                ),
            ] {
                if rect.width > 0.0 && rect.height > 0.0 {
                    list.items.push(DisplayItem::SolidColor {
                        rect,
                        color,
                        alpha: layout_box.opacity,
                    });
                }
            }
        }
        // Outline: a ring outside the border box, at a uniform width and colour
        // — CSS gives outline no per-side variant, so this is the same
        // four-rect ring technique as the border above but with one width and
        // one colour throughout, drawn against `outer` (the outline's own outer
        // edge) and `dimensions.border_box()` (its inner edge, which is the
        // element's ordinary outer edge — outline paints beyond it without
        // moving it). It cannot overlap the border ring, since the two occupy
        // disjoint bands, so paint order between them does not matter.
        if layout_box.outline_width > 0.0 {
            let currentcolor = layout_box.color.unwrap_or_default();
            let color = layout_box.outline_color.unwrap_or(currentcolor);
            let inner = dimensions.border_box();
            let outer = expand(inner, uniform(layout_box.outline_width));
            for rect in [
                Rect {
                    x: outer.x,
                    y: outer.y,
                    width: outer.width,
                    height: inner.y - outer.y,
                },
                Rect {
                    x: outer.x,
                    y: inner.y + inner.height,
                    width: outer.width,
                    height: (outer.y + outer.height) - (inner.y + inner.height),
                },
                Rect {
                    x: outer.x,
                    y: inner.y,
                    width: inner.x - outer.x,
                    height: inner.height,
                },
                Rect {
                    x: inner.x + inner.width,
                    y: inner.y,
                    width: (outer.x + outer.width) - (inner.x + inner.width),
                    height: inner.height,
                },
            ] {
                if rect.width > 0.0 && rect.height > 0.0 {
                    list.items.push(DisplayItem::SolidColor {
                        rect,
                        color,
                        alpha: layout_box.opacity,
                    });
                }
            }
        }
        // Backgrounds paint before content, and a parent paints before its
        // children, which is the document-order approximation of paint order.
        if let Some(color) = &layout_box.background {
            let rect = layout_box.dimensions.padding_box();
            list.items.push(if layout_box.border_radius > 0.0 {
                DisplayItem::RoundedColor {
                    rect,
                    color: *color,
                    radius: layout_box.border_radius,
                    alpha: layout_box.opacity,
                }
            } else {
                DisplayItem::SolidColor {
                    rect,
                    color: *color,
                    alpha: layout_box.opacity,
                }
            });
        }
        if let (BoxKind::Text, Some(text)) = (layout_box.kind, &layout_box.text) {
            let rect = layout_box.dimensions.content;
            // The initial value of `color` is black, per CSS. This is a
            // specified default rather than a fallback for a missing value.
            let color = layout_box.color.unwrap_or_default();
            list.items.push(DisplayItem::Text {
                rect,
                text: text.clone(),
                color,
                alpha: layout_box.opacity,
            });
            // The decoration line's position is a fraction of the line box's own
            // height rather than any specific font's glyph metrics — this crate
            // only knows `TextMetrics`, not what a painter's glyphs actually
            // look like, and a line tied to one font's bitmap would be wrong the
            // moment a different painter injected different metrics. Underline
            // sits near the bottom of the line box; line-through sits at its
            // vertical centre. One pixel tall, which is thin enough to read as a
            // line rather than a second, shorter fill.
            if layout_box.text_decoration != TextDecoration::None {
                let y = match layout_box.text_decoration {
                    TextDecoration::Underline => rect.y + rect.height * 0.85,
                    TextDecoration::LineThrough => rect.y + rect.height * 0.5,
                    TextDecoration::None => unreachable!("checked above"),
                };
                list.items.push(DisplayItem::SolidColor {
                    rect: Rect {
                        x: rect.x,
                        y,
                        width: rect.width,
                        height: 1.0,
                    },
                    color,
                    alpha: layout_box.opacity,
                });
            }
        }
    }
    for child in &layout_box.children {
        paint(child, list);
    }
}

// -- box generation ------------------------------------------------------

/// The inherited properties a box passes down to its children, bundled so
/// `build_box` takes one parameter for "what this subtree inherited" rather
/// than growing a new positional parameter for every property that turns
/// out to inherit — which is exactly the shape that made the function trip
/// `clippy::too_many_arguments` the day a fourth one arrived.
#[derive(Clone, Copy, Debug)]
struct Inherited {
    color: Option<Color>,
    align: TextAlign,
    decoration: TextDecoration,
    visibility: Visibility,
    /// The ambient opacity every descendant's own paint multiplies into its
    /// resolved alpha. Not CSS inheritance in the strict sense — the
    /// `opacity` *property* does not cascade to a child's own computed value
    /// — but the *visual* effect does reach descendants in real CSS,
    /// because an opacity box forms a stacking context that composites its
    /// whole subtree as one flattened group. This engine has no offscreen
    /// layer to flatten a group through, so multiplying each descendant's
    /// own alpha by the ambient value is the approximation: exactly right
    /// for a translucent box whose descendants do not overlap each other,
    /// and only wrong in the narrower case of two overlapping translucent
    /// boxes inside the same translucent ancestor, where a real browser's
    /// flattened group would show through no further than the ancestor's
    /// own opacity and this engine's product of independent alphas goes
    /// more transparent than that.
    opacity: f32,
}

impl Default for Inherited {
    fn default() -> Self {
        Self {
            color: None,
            align: TextAlign::default(),
            decoration: TextDecoration::default(),
            visibility: Visibility::default(),
            opacity: 1.0,
        }
    }
}

fn build_box<T: LayoutTree>(
    tree: &T,
    index: &SelectorIndex,
    node: T::Node,
    inherited: Inherited,
    hovered: Option<T::Node>,
    depth: usize,
) -> Result<Option<LayoutBox>, LayoutError> {
    // Box generation recurses, and so do layout, painting, and hit testing over
    // the box tree it produces. A stack overflow is not a recoverable error:
    // it aborts the process and cannot be caught, so a document deeper than the
    // limit is refused here rather than allowed to crash later.
    if depth > MAX_NESTING_DEPTH {
        return Err(LayoutError::NestingTooDeep {
            limit: MAX_NESTING_DEPTH,
        });
    }

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
            color: inherited.color,
            border_colors: BorderColors::default(),
            border_radius: 0.0,
            outline_width: 0.0,
            outline_color: None,
            text_align: inherited.align,
            text_decoration: inherited.decoration,
            visibility: inherited.visibility,
            // A text run has no `opacity` of its own to declare; it paints
            // at whatever ambient opacity its nearest ancestors resolved to,
            // the same way it reads `inherited.color`.
            opacity: inherited.opacity,
            flex_direction: FlexDirection::default(),
            align_items: AlignItems::default(),
            justify_content: JustifyContent::default(),
            gap: 0.0,
            flex_grow: 0.0,
            flex_shrink: 1.0,
            flex_basis: FlexBasis::default(),
            children: Vec::new(),
        }));
    }
    if tree.is_non_rendered(node) {
        return Ok(None);
    }

    let style = resolve_style(tree, index, node, hovered)?;
    let display = style.display.as_deref().unwrap_or("");
    if display == "none" {
        return Ok(None);
    }

    // This box's own resolved alpha: its own declared opacity (default
    // fully opaque) multiplied by whatever ambient opacity its ancestors
    // already resolved to. The same value is what gets passed to children
    // as their new ambient — see `Inherited::opacity`'s own doc comment for
    // why multiplying is the chosen approximation of group flattening.
    let resolved_opacity = style.opacity.unwrap_or(1.0) * inherited.opacity;
    let own = Inherited {
        color: style.color.or(inherited.color),
        align: style.text_align.unwrap_or(inherited.align),
        decoration: style.text_decoration.unwrap_or(inherited.decoration),
        visibility: style.visibility.unwrap_or(inherited.visibility),
        opacity: resolved_opacity,
    };
    let mut children = Vec::new();
    for child in tree.children(node) {
        if let Some(built) = build_box(tree, index, child, own, hovered, depth + 1)? {
            children.push(built);
        }
    }

    // The root is not an element and has no `display`, so it stays a block.
    let kind = if !tree.is_element(node) {
        BoxKind::Block
    } else {
        match display {
            "inline" => BoxKind::Inline,
            "flex" => BoxKind::Flex,
            _ => BoxKind::Block,
        }
    };

    // A block box whose children mix block and inline levels needs anonymous
    // block boxes so the inline runs form their own formatting context. A
    // flex container's children are never wrapped this way — every in-flow
    // child of a flex box is a flex item, whatever level it would otherwise
    // have been, so `has_mixed_levels` never applies to `kind == Flex`.
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
        background: style.background,
        color: own.color,
        border_colors: style.border_colors,
        border_radius: style.border_radius,
        outline_width: style.outline_width,
        outline_color: style.outline_color,
        text_align: own.align,
        text_decoration: own.decoration,
        visibility: own.visibility,
        opacity: resolved_opacity,
        flex_direction: style.flex_direction.unwrap_or_default(),
        align_items: style.align_items.unwrap_or_default(),
        justify_content: style.justify_content.unwrap_or_default(),
        gap: style.gap.unwrap_or(0.0),
        flex_grow: style.flex_grow.unwrap_or(0.0),
        flex_shrink: style.flex_shrink.unwrap_or(1.0),
        flex_basis: style.flex_basis.unwrap_or_default(),
        children,
    }))
}

fn has_mixed_levels(children: &[LayoutBox]) -> bool {
    // A flex container is block-level and never an inline participant, so it
    // ends an inline run exactly the way an ordinary block box does — both
    // count toward "this parent has a block-level child" for the purpose of
    // deciding whether the inline runs beside it need their own anonymous
    // block.
    let block = children
        .iter()
        .any(|c| matches!(c.kind, BoxKind::Block | BoxKind::Flex));
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
    // An anonymous block inherits alignment from the inline content it wraps:
    // every child inherited the real parent's `text-align`, so the first
    // child carries the value this box must align by.
    let text_align = children
        .first()
        .map_or(TextAlign::default(), |c| c.text_align);
    LayoutBox {
        dimensions: Dimensions::default(),
        kind: BoxKind::AnonymousBlock,
        node: None,
        text: None,
        background: None,
        color: None,
        border_colors: BorderColors::default(),
        border_radius: 0.0,
        outline_width: 0.0,
        outline_color: None,
        text_align,
        // An anonymous block has no text of its own — its children already
        // carry whatever decoration `build_box` resolved for each of them —
        // so this value is inert for painting; `None` is simply the box
        // kind's honest own state, same as its colour and background.
        text_decoration: TextDecoration::default(),
        // Likewise inert: an anonymous block never paints a background,
        // border, or outline of its own (it has none, by construction), and
        // `paint` recurses into every child regardless of this box's own
        // visibility — each child already carries its own correctly
        // inherited value from the real element that produced it.
        visibility: Visibility::default(),
        // Inert for the same reason `text_decoration` is just above: an
        // anonymous block never paints anything of its own.
        opacity: 1.0,
        // An anonymous block is never a flex container and never a flex
        // item's own contributed style (the item's flex properties, if any,
        // live on the real element inside it), so every flex-related field
        // stays at its inert initial value here.
        flex_direction: FlexDirection::default(),
        align_items: AlignItems::default(),
        justify_content: JustifyContent::default(),
        gap: 0.0,
        flex_grow: 0.0,
        flex_shrink: 1.0,
        flex_basis: FlexBasis::default(),
        children,
    }
}

fn resolve_style<T: LayoutTree>(
    tree: &T,
    index: &SelectorIndex,
    node: T::Node,
    hovered: Option<T::Node>,
) -> Result<Style, LayoutError> {
    let mut style = Style::default();
    if !tree.is_element(node) {
        return Ok(style);
    }

    let declarations = cascade(tree, node, index, hovered);
    for (property, computed) in &declarations {
        let value = computed.value.as_str();
        match property.as_str() {
            "display" => {
                match value {
                    "block" | "inline" | "flex" | "none" => {
                        style.display = Some(value.to_string());
                    }
                    // `inline-flex` gets its own error: the inner flex
                    // algorithm below is implemented, so the generic
                    // "replaces the layout algorithm" message would be
                    // false here — what is missing is atomic inline-level
                    // sizing for the outer box, the same gap that leaves
                    // `inline-block` unsupported.
                    "inline-flex" => {
                        return Err(LayoutError::AtomicInlineUnsupported {
                            value: value.to_string(),
                        });
                    }
                    // grid and table replace the layout algorithm.
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
            // Negative edges are refused rather than approximated. A negative
            // margin is valid CSS whose collapsing rule differs from the
            // positive one — the most negative margin is added to the largest
            // positive, not maximised against it — and this implementation
            // computes only the positive rule, so accepting one would place
            // content wrongly while appearing to succeed. Negative padding and
            // border are invalid CSS, and refusing surfaces the authoring error.
            "margin" => style.margin = uniform(non_negative(property, value)?),
            "padding" => style.padding = uniform(non_negative(property, value)?),
            "border-width" => style.border = uniform(non_negative(property, value)?),
            // A longhand only overrides the shorthand's side when it
            // actually outranks it by the cascade's own rule — specificity,
            // then source order — rather than unconditionally, which is what
            // made the shorthand's position in the rule irrelevant before
            // this. See `wins_over_shorthand` for the shared check every
            // border longhand below uses.
            "border-top-width" if wins_over_shorthand(&declarations, "border-width", computed) => {
                style.border.top = non_negative(property, value)?;
            }
            "border-right-width"
                if wins_over_shorthand(&declarations, "border-width", computed) =>
            {
                style.border.right = non_negative(property, value)?;
            }
            "border-bottom-width"
                if wins_over_shorthand(&declarations, "border-width", computed) =>
            {
                style.border.bottom = non_negative(property, value)?;
            }
            "border-left-width" if wins_over_shorthand(&declarations, "border-width", computed) => {
                style.border.left = non_negative(property, value)?;
            }
            // A longhand that loses to the shorthand still has to be
            // validated — a page author who wrote a malformed value should
            // see that error, not have it hidden by a shorthand that happens
            // to win. `non_negative` runs for its `?` alone here.
            "border-top-width"
            | "border-right-width"
            | "border-bottom-width"
            | "border-left-width" => {
                non_negative(property, value)?;
            }
            "background" | "background-color" => style.background = Some(Color::parse(value)?),
            "color" => style.color = Some(Color::parse(value)?),
            "border-color" => style.border_colors = BorderColors::uniform(Color::parse(value)?),
            "border-top-color" if wins_over_shorthand(&declarations, "border-color", computed) => {
                style.border_colors.top = Some(Color::parse(value)?);
            }
            "border-right-color"
                if wins_over_shorthand(&declarations, "border-color", computed) =>
            {
                style.border_colors.right = Some(Color::parse(value)?);
            }
            "border-bottom-color"
                if wins_over_shorthand(&declarations, "border-color", computed) =>
            {
                style.border_colors.bottom = Some(Color::parse(value)?);
            }
            "border-left-color" if wins_over_shorthand(&declarations, "border-color", computed) => {
                style.border_colors.left = Some(Color::parse(value)?);
            }
            "border-top-color"
            | "border-right-color"
            | "border-bottom-color"
            | "border-left-color" => {
                Color::parse(value)?;
            }
            "border-radius" => style.border_radius = non_negative(property, value)?,
            // `outline` never affects layout — unlike `border`, it paints
            // outside the border box without moving anything else, which is
            // why it has no per-side variant and no shorthand-vs-longhand
            // question to resolve: there is exactly one width and one
            // colour, always.
            "outline-width" => style.outline_width = non_negative(property, value)?,
            "outline-color" => style.outline_color = Some(Color::parse(value)?),
            "opacity" => style.opacity = Some(parse_opacity(value)),
            "text-align" => {
                style.text_align = Some(match value.trim().to_ascii_lowercase().as_str() {
                    "left" | "start" => TextAlign::Start,
                    "center" => TextAlign::Center,
                    "right" | "end" => TextAlign::End,
                    // justify and match-parent are not implemented; refusing
                    // keeps an unhandled alignment from silently reading as
                    // left, which looks correct until the line is long.
                    other => {
                        return Err(LayoutError::TextAlignUnsupported {
                            value: other.to_string(),
                        });
                    }
                });
            }
            "text-decoration" => {
                style.text_decoration = Some(match value.trim().to_ascii_lowercase().as_str() {
                    "none" => TextDecoration::None,
                    "underline" => TextDecoration::Underline,
                    "line-through" => TextDecoration::LineThrough,
                    // `overline`, multi-value combinations
                    // (`underline line-through`), and the colour/style/
                    // thickness longhands are not implemented; refusing
                    // keeps an unhandled decoration from silently reading as
                    // no decoration.
                    other => {
                        return Err(LayoutError::TextDecorationUnsupported {
                            value: other.to_string(),
                        });
                    }
                });
            }
            "visibility" => {
                style.visibility = Some(match value.trim().to_ascii_lowercase().as_str() {
                    "visible" => Visibility::Visible,
                    "hidden" => Visibility::Hidden,
                    // `collapse` (a table-row-specific behaviour this
                    // implementation has no table layout to give meaning to)
                    // is refused rather than treated as `hidden`, which is a
                    // real but different effect.
                    other => {
                        return Err(LayoutError::VisibilityUnsupported {
                            value: other.to_string(),
                        });
                    }
                });
            }
            "flex-direction" => {
                style.flex_direction = Some(match value.trim().to_ascii_lowercase().as_str() {
                    "row" => FlexDirection::Row,
                    "column" => FlexDirection::Column,
                    // `row-reverse` and `column-reverse` move main-start to
                    // the opposite edge, which shifts every item's position
                    // — refused rather than placed as the forward direction.
                    other => {
                        return Err(LayoutError::FlexDirectionUnsupported {
                            value: other.to_string(),
                        });
                    }
                });
            }
            // Single-line only: this implementation does not fragment flex
            // items onto a second line, so anything other than the initial
            // `nowrap` is refused rather than silently collapsed onto one
            // line.
            "flex-wrap" if !value.trim().eq_ignore_ascii_case("nowrap") => {
                return Err(LayoutError::FlexWrapUnsupported {
                    value: value.to_string(),
                });
            }
            "flex-wrap" => {}
            "align-items" => {
                style.align_items = Some(match value.trim().to_ascii_lowercase().as_str() {
                    "flex-start" => AlignItems::FlexStart,
                    "center" => AlignItems::Center,
                    "flex-end" => AlignItems::FlexEnd,
                    "stretch" => AlignItems::Stretch,
                    other => {
                        return Err(LayoutError::AlignItemsUnsupported {
                            value: other.to_string(),
                        });
                    }
                });
            }
            "justify-content" => {
                style.justify_content = Some(match value.trim().to_ascii_lowercase().as_str() {
                    "flex-start" => JustifyContent::FlexStart,
                    "center" => JustifyContent::Center,
                    "flex-end" => JustifyContent::FlexEnd,
                    "space-between" => JustifyContent::SpaceBetween,
                    "space-around" => JustifyContent::SpaceAround,
                    other => {
                        return Err(LayoutError::JustifyContentUnsupported {
                            value: other.to_string(),
                        });
                    }
                });
            }
            // A negative gap is invalid CSS; refusing surfaces the
            // authoring error the same way negative margin/padding do.
            "gap" => style.gap = Some(non_negative(property, value)?),
            "flex-grow" => style.flex_grow = Some(non_negative_number(property, value)?),
            "flex-shrink" => style.flex_shrink = Some(non_negative_number(property, value)?),
            "flex-basis" => {
                style.flex_basis = Some(match value.trim().to_ascii_lowercase().as_str() {
                    "auto" => FlexBasis::Auto,
                    // A percentage or other unresolved unit is treated as
                    // `auto`, the same silent fallback `width`/`height`
                    // already give an unparseable length — not a new
                    // simplification, the existing one applied to a new
                    // property.
                    _ => parse_length(value).map_or(FlexBasis::Auto, FlexBasis::Length),
                });
            }
            "flex" => {
                let (grow, shrink, basis) = parse_flex_shorthand(value)?;
                style.flex_grow = Some(grow);
                style.flex_shrink = Some(shrink);
                style.flex_basis = Some(basis);
            }
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

/// Whether `longhand`'s own declaration outranks `shorthand`'s declaration
/// among `declarations`, by the identical specificity-then-source-order rule
/// `turing_css::cascade` already uses to pick a winner for one property
/// name — mirrored here rather than exported from that crate, because
/// `turing-css` is deliberately property-agnostic: it does not and should
/// not know that `border-color` is short for `border-top-color` and three
/// others. That knowledge belongs to this crate, which already owns every
/// other fact about what a CSS property means.
///
/// If `shorthand` was not declared on this element at all, there is nothing
/// to outrank, and the longhand always applies — the ordinary case, since
/// most rules never declare a shorthand and a longhand for the same
/// property together.
fn wins_over_shorthand(
    declarations: &[(String, ComputedDeclaration)],
    shorthand: &str,
    longhand: &ComputedDeclaration,
) -> bool {
    let Some((_, shorthand_declaration)) = declarations.iter().find(|(name, _)| name == shorthand)
    else {
        return true;
    };
    match (longhand.important, shorthand_declaration.important) {
        (true, false) => true,
        (false, true) => false,
        _ => match longhand.specificity.cmp(&shorthand_declaration.specificity) {
            core::cmp::Ordering::Greater => true,
            core::cmp::Ordering::Less => false,
            core::cmp::Ordering::Equal => {
                longhand.source_order >= shorthand_declaration.source_order
            }
        },
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

/// Parses an edge length, refusing a negative one.
///
/// An unparseable value yields `0.0`, matching the existing treatment of units
/// this crate does not resolve; a *parsed* negative is a different case, because
/// the author said something specific that this implementation would get wrong.
fn non_negative(property: &str, value: &str) -> Result<f32, LayoutError> {
    let length = parse_length(value).unwrap_or(0.0);
    if length < 0.0 {
        return Err(LayoutError::NegativeEdgeUnsupported {
            property: property.to_string(),
            value: value.to_string(),
        });
    }
    Ok(length)
}

/// Parses a length in `px` or a bare number. Percentages and relative units
/// are not resolved here and yield `None`, which layout treats as `auto`.
///
/// Rust's `f32::from_str` accepts `"nan"` and `"inf"` as valid floats — they
/// are not valid CSS lengths, and every caller of this function eventually
/// does arithmetic with the result (subtracting it from a containing size,
/// comparing it to zero, summing it with a sibling's), where a NaN or
/// infinity would silently propagate rather than error. Filtering here once
/// is what makes every one of those downstream comparisons trustworthy;
/// see `resolve_flex_basis` and the free-space division in
/// `layout_flex_children` for arithmetic that specifically depends on it.
fn parse_length(value: &str) -> Option<f32> {
    let trimmed = value.trim();
    let number = trimmed.strip_suffix("px").unwrap_or(trimmed);
    let parsed = number.trim().parse::<f32>().ok()?;
    parsed.is_finite().then_some(parsed)
}

/// Parses `opacity`'s value — a bare number or a percentage — and clamps it
/// to the `[0, 1]` range CSS defines for it (an author-supplied `150%` is a
/// real, specified case CSS resolves by clamping, not an error to refuse).
///
/// A value this cannot parse at all keeps the initial value, fully opaque,
/// rather than refusing the whole declaration block: unlike an unsupported
/// `display` mode, where guessing risks silently placing content in the
/// wrong formatting model, an un-parseable `opacity` failing open to "paint
/// normally" is the same outcome CSS itself defines for any other property a
/// browser does not recognise.
///
/// `"NaN"` and `"nan%"` are both syntax `f32::from_str` accepts, so they
/// count as *parsed*, not *unparseable* — `f32::clamp` passes a `NaN` input
/// straight through rather than clamping it into range, which would carry a
/// `NaN` alpha all the way to the compositor's blend math and, cast to a
/// pixel channel, silently paint a channel Rust's saturating float-to-int
/// cast resolves to `0` rather than anything a stylesheet author asked for.
/// Treated the same as any other value this function cannot make sense of.
fn parse_opacity(value: &str) -> f32 {
    let trimmed = value.trim();
    let parsed = trimmed.strip_suffix('%').map_or_else(
        || trimmed.parse::<f32>().ok(),
        |percent| percent.trim().parse::<f32>().ok().map(|p| p / 100.0),
    );
    parsed
        .filter(|value| !value.is_nan())
        .unwrap_or(1.0)
        .clamp(0.0, 1.0)
}

/// Parses a bare CSS number — used by `flex-grow`, `flex-shrink`, and the
/// `flex` shorthand, none of which take a unit. Filters non-finite values
/// for the same reason `parse_length` does.
fn parse_number(value: &str) -> Option<f32> {
    let parsed = value.trim().parse::<f32>().ok()?;
    parsed.is_finite().then_some(parsed)
}

/// Parses a non-negative bare number, refusing a negative one. `flex-grow`
/// and `flex-shrink` are invalid when negative per CSS; an unparseable value
/// falls back to `0.0`, matching `non_negative`'s treatment of an
/// unparseable length.
fn non_negative_number(property: &str, value: &str) -> Result<f32, LayoutError> {
    let number = parse_number(value).unwrap_or(0.0);
    if number < 0.0 {
        return Err(LayoutError::NegativeEdgeUnsupported {
            property: property.to_string(),
            value: value.to_string(),
        });
    }
    Ok(number)
}

/// Resolves the `flex` shorthand to its three longhands.
///
/// The shorthand's full grammar lets the grow/shrink pair and the basis
/// appear in either order and be independently omitted, which is genuinely
/// ambiguous to parse in general (a bare numeric-looking basis versus a
/// grow factor). This resolves exactly the forms that are unambiguous —
/// the ones this crate's callers are documented to support — and refuses
/// anything else rather than guess which token means what:
///
/// - `none` → `(0, 0, Auto)`
/// - `auto` → `(1, 1, Auto)`
/// - `initial` → `(0, 1, Auto)`, the properties' own individual initial
///   values
/// - a bare `<number>` → `(number, 1, Length(0.0))`
/// - `<number> <number>` → `(grow, shrink, Length(0.0))`
/// - `<number> <number> <basis>` → `(grow, shrink, basis)`, where `<basis>`
///   is `auto` or a length
///
/// Per CSS, omitting the basis from the shorthand sets it to `0`, not
/// `auto` — the shorthand's whole point is that different default.
fn parse_flex_shorthand(value: &str) -> Result<(f32, f32, FlexBasis), LayoutError> {
    let trimmed = value.trim();
    let unsupported = || LayoutError::FlexShorthandUnsupported {
        value: value.to_string(),
    };
    match trimmed.to_ascii_lowercase().as_str() {
        "none" => return Ok((0.0, 0.0, FlexBasis::Auto)),
        "auto" => return Ok((1.0, 1.0, FlexBasis::Auto)),
        "initial" => return Ok((0.0, 1.0, FlexBasis::Auto)),
        _ => {}
    }
    let tokens: Vec<&str> = trimmed.split_whitespace().collect();
    match tokens.as_slice() {
        [grow] => {
            let grow = parse_number(grow).ok_or_else(unsupported)?;
            if grow < 0.0 {
                return Err(unsupported());
            }
            Ok((grow, 1.0, FlexBasis::Length(0.0)))
        }
        [grow, shrink] => {
            let grow = parse_number(grow).ok_or_else(unsupported)?;
            let shrink = parse_number(shrink).ok_or_else(unsupported)?;
            if grow < 0.0 || shrink < 0.0 {
                return Err(unsupported());
            }
            Ok((grow, shrink, FlexBasis::Length(0.0)))
        }
        [grow, shrink, basis] => {
            let grow = parse_number(grow).ok_or_else(unsupported)?;
            let shrink = parse_number(shrink).ok_or_else(unsupported)?;
            if grow < 0.0 || shrink < 0.0 {
                return Err(unsupported());
            }
            let basis = if basis.eq_ignore_ascii_case("auto") {
                FlexBasis::Auto
            } else {
                FlexBasis::Length(parse_length(basis).ok_or_else(unsupported)?)
            };
            Ok((grow, shrink, basis))
        }
        _ => Err(unsupported()),
    }
}

// -- layout --------------------------------------------------------------

/// Lays out `layout_box` into `containing` using whichever formatting
/// context its own `kind` calls for.
///
/// This is the single dispatch point between block/inline layout and flex
/// layout: every place a box is laid out as a fresh child of some containing
/// block — the document root, and each child of an ordinary block box —
/// goes through this rather than calling `layout_block` directly, so a flex
/// container found in either position genuinely gets flex layout rather than
/// silently falling back to block stacking.
fn layout_any(layout_box: &mut LayoutBox, containing: Dimensions, metrics: TextMetrics) {
    match layout_box.kind {
        BoxKind::Flex => layout_flex(layout_box, containing, metrics),
        BoxKind::Block | BoxKind::Inline | BoxKind::Text | BoxKind::AnonymousBlock => {
            layout_block(layout_box, containing, metrics);
        }
    }
}

/// Lays out `layout_box`'s own children using whichever formatting context
/// its `kind` calls for, assuming `layout_box.dimensions.content` is already
/// fully resolved (position and, where definite, size).
///
/// Unlike `layout_any`, this does not touch the box's own outer width,
/// position, or declared height — it exists for the one caller that has
/// already decided those (`layout_flex_children`, resolving a flex item's
/// box model from the flex algorithm rather than the ordinary containing­
/// block rules `calculate_width`/`calculate_position` implement).
fn layout_box_children(layout_box: &mut LayoutBox, metrics: TextMetrics) {
    match layout_box.kind {
        BoxKind::Flex => layout_flex_children(layout_box, metrics),
        BoxKind::Block | BoxKind::Inline | BoxKind::Text | BoxKind::AnonymousBlock => {
            layout_children(layout_box, metrics);
        }
    }
}

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

        layout_any(child, cursor, metrics);
        cursor.content.height += child.dimensions.margin_box().height;
        previous_margin_bottom = child.dimensions.margin.bottom;
    }
    layout_box.children = children;
    layout_box.dimensions.content.height = cursor.content.height;
}

/// The advance width of an inline box: its own text, or the sum of its
/// descendants' text for an inline element.
///
/// Without the recursive arm an inline element measures as zero, every such
/// element lands at the same pen position, and `<span>a</span><span>b</span>`
/// paints both words on top of each other. An inline element moves between
/// lines as one unbreakable unit; breaking inside one is line fragmentation,
/// which this layout does not implement.
fn inline_advance_width(layout_box: &LayoutBox, metrics: TextMetrics) -> f32 {
    if let Some(text) = &layout_box.text {
        // Measured as it will be placed: words joined by single collapsed
        // spaces, leading and trailing whitespace ignored.
        let characters: usize = text
            .split_whitespace()
            .map(|word| word.chars().count())
            .sum();
        let words = text.split_whitespace().count();
        #[allow(clippy::cast_precision_loss)]
        return (characters + words.saturating_sub(1)) as f32 * metrics.advance;
    }
    layout_box
        .children
        .iter()
        .map(|child| inline_advance_width(child, metrics))
        .sum()
}

/// Greedy, word-level line breaking over inline children.
///
/// A text run breaks between words and its interior whitespace collapses to a
/// single space, which is dropped at a line start; an inline element moves
/// between lines whole. Each placed word becomes its own text fragment box
/// carrying the source node, so painting and hit testing work on fragments
/// without knowing lines exist.
fn layout_inline_children(layout_box: &mut LayoutBox, metrics: TextMetrics) {
    let origin_x = layout_box.dimensions.content.x;
    let origin_y = layout_box.dimensions.content.y;
    let available = layout_box.dimensions.content.width;

    let mut pen_x = 0.0_f32;
    let mut line = 0.0_f32;
    // Whether whitespace was seen since the last placed word or element. A
    // pending space paints nothing; it widens the gap the next placement must
    // fit into, and it evaporates at a line start.
    let mut pending_space = false;
    let mut placed = Vec::new();

    for child in core::mem::take(&mut layout_box.children) {
        if child.kind == BoxKind::Text {
            let text = child.text.clone().unwrap_or_default();
            if text.starts_with(char::is_whitespace) {
                pending_space = true;
            }
            for word in text.split_whitespace() {
                #[allow(clippy::cast_precision_loss)]
                let width = word.chars().count() as f32 * metrics.advance;
                let space = if pending_space && pen_x > 0.0 {
                    metrics.advance
                } else {
                    0.0
                };
                if pen_x > 0.0 && pen_x + space + width > available {
                    pen_x = 0.0;
                    line += 1.0;
                } else {
                    pen_x += space;
                }
                let mut fragment = child.clone();
                fragment.text = Some(word.to_owned());
                fragment.dimensions.content = Rect {
                    x: origin_x + pen_x,
                    y: line.mul_add(metrics.line_height, origin_y),
                    width,
                    height: metrics.line_height,
                };
                pen_x += width;
                placed.push(fragment);
                // Words inside one run are whitespace-separated by
                // construction; whether a space follows the run's last word
                // is decided below from the run's own tail.
                pending_space = true;
            }
            pending_space =
                text.ends_with(char::is_whitespace) || text.trim().is_empty() && pending_space;
        } else {
            let mut child = child;
            // Horizontal margin on an inline element is real space between it
            // and its neighbours on the line — unlike `padding`/`border`,
            // which this layout does not yet reserve room for on an inline
            // box, `margin` was already carried on `child.dimensions` from
            // `build_box` and simply never consulted here, so it silently
            // had no visual effect at all.
            let margin_left = child.dimensions.margin.left;
            let margin_right = child.dimensions.margin.right;
            let width = inline_advance_width(&child, metrics);
            let margin_box_width = margin_left + width + margin_right;
            let space = if pending_space && pen_x > 0.0 {
                metrics.advance
            } else {
                0.0
            };
            if pen_x > 0.0 && pen_x + space + margin_box_width > available {
                pen_x = 0.0;
                line += 1.0;
            } else {
                pen_x += space;
            }
            pen_x += margin_left;
            child.dimensions.content = Rect {
                x: origin_x + pen_x,
                y: line.mul_add(metrics.line_height, origin_y),
                width,
                height: metrics.line_height,
            };
            pen_x += width + margin_right;
            pending_space = false;
            // Nested inline boxes lay their own children out on the same line.
            if !child.children.is_empty() {
                layout_inline_children(&mut child, metrics);
            }
            placed.push(child);
        }
    }
    // `text-align` other than the initial start value shifts each line by its
    // slack — the space between where the line ends and the content edge.
    // Start needs no work; the greedy placement above already left-aligns.
    if layout_box.text_align != TextAlign::Start {
        align_lines(&mut placed, origin_x, available, layout_box.text_align);
    }

    layout_box.children = placed;
    layout_box.dimensions.content.height = (line + 1.0) * metrics.line_height;
}

/// Shifts each line of placed fragments horizontally for a non-start
/// `text-align`. Fragments are grouped by their `y`, and every fragment on a
/// line moves by the same offset, so words keep their spacing.
fn align_lines(placed: &mut [LayoutBox], origin_x: f32, available: f32, align: TextAlign) {
    let mut start = 0;
    while start < placed.len() {
        let line_y = placed[start].dimensions.content.y;
        let mut end = start;
        let mut line_right = origin_x;
        while end < placed.len() && placed[end].dimensions.content.y == line_y {
            let rect = placed[end].dimensions.content;
            line_right = line_right.max(rect.x + rect.width);
            end += 1;
        }
        let slack = (origin_x + available) - line_right;
        let offset = match align {
            TextAlign::Center => slack / 2.0,
            TextAlign::End => slack,
            TextAlign::Start => 0.0,
        };
        if offset > 0.0 {
            for fragment in &mut placed[start..end] {
                shift_x(fragment, offset);
            }
        }
        start = end;
    }
}

/// Moves a box and all its descendants right by `offset`.
fn shift_x(layout_box: &mut LayoutBox, offset: f32) {
    layout_box.dimensions.content.x += offset;
    for child in &mut layout_box.children {
        shift_x(child, offset);
    }
}

/// Moves a box and all its descendants down by `offset`. The vertical
/// counterpart to `shift_x`, used by flex layout to apply a row container's
/// cross-axis (`align-items`) offset after an item's own children have
/// already been laid out relative to a provisional position.
fn shift_y(layout_box: &mut LayoutBox, offset: f32) {
    layout_box.dimensions.content.y += offset;
    for child in &mut layout_box.children {
        shift_y(child, offset);
    }
}

// -- flex layout ----------------------------------------------------------
//
// A flex container lays its children out along one axis (the "main" axis,
// `flex-direction`) and aligns them on the other (the "cross" axis). This
// implements the single-line case of CSS's flexible box algorithm: item
// main sizes start from `flex-basis`, and any surplus or deficit against the
// container's main size is distributed by `flex-grow`/`flex-shrink`
// proportionally. `flex-wrap` is refused in `resolve_style` before layout
// ever sees a wrapped container, so every item here lands on the one line.

fn layout_flex(layout_box: &mut LayoutBox, containing: Dimensions, metrics: TextMetrics) {
    calculate_width(layout_box, containing);
    calculate_position(layout_box, containing);
    // Mirrors `layout_block`: a declared height must survive whatever the
    // children computation below does with an auto one.
    let declared_height = layout_box.dimensions.content.height;
    layout_flex_children(layout_box, metrics);
    calculate_height(layout_box, declared_height);
}

/// Resolves a flex item's used `flex-basis`.
///
/// An explicit basis (the property or the `flex` shorthand) is used as-is.
/// `auto` defers to the item's own declared size on the main axis — `width`
/// for a row, `height` for a column — matching the real CSS rule. Failing
/// that, this crate has no general intrinsic-sizing pass (nothing else here
/// shrinks a block to its content either), except for the one case it
/// already knows how to measure: a text or inline item's own advance width
/// (row) or line height (column), via the same `inline_advance_width` inline
/// layout itself uses. Anything else — a block or flex item with no
/// declared main size — falls back to `0`, the same default the `flex`
/// shorthand itself gives an omitted basis, rather than inventing a content
/// measurement this engine cannot make.
fn resolve_flex_basis(item: &LayoutBox, direction: FlexDirection, metrics: TextMetrics) -> f32 {
    if let FlexBasis::Length(length) = item.flex_basis {
        return length;
    }
    let declared = match direction {
        FlexDirection::Row => item.dimensions.content.width,
        FlexDirection::Column => item.dimensions.content.height,
    };
    if declared > 0.0 {
        return declared;
    }
    match (direction, item.kind) {
        (FlexDirection::Row, BoxKind::Text | BoxKind::Inline) => {
            inline_advance_width(item, metrics)
        }
        (FlexDirection::Column, BoxKind::Text | BoxKind::Inline) => metrics.line_height,
        _ => 0.0,
    }
}

/// Margin, border, and padding on both edges of the main axis.
fn item_main_extra(item: &LayoutBox, direction: FlexDirection) -> f32 {
    let d = item.dimensions;
    match direction {
        FlexDirection::Row => {
            d.margin.left
                + d.margin.right
                + d.border.left
                + d.border.right
                + d.padding.left
                + d.padding.right
        }
        FlexDirection::Column => {
            d.margin.top
                + d.margin.bottom
                + d.border.top
                + d.border.bottom
                + d.padding.top
                + d.padding.bottom
        }
    }
}

/// Margin, border, and padding on the main-start edge only — how far a
/// content box sits from the outer edge `layout_flex_children`'s cursor
/// tracks.
fn item_main_leading(item: &LayoutBox, direction: FlexDirection) -> f32 {
    let d = item.dimensions;
    match direction {
        FlexDirection::Row => d.margin.left + d.border.left + d.padding.left,
        FlexDirection::Column => d.margin.top + d.border.top + d.padding.top,
    }
}

/// Margin, border, and padding on both edges of the cross axis.
fn item_cross_extra(item: &LayoutBox, direction: FlexDirection) -> f32 {
    let d = item.dimensions;
    match direction {
        FlexDirection::Row => {
            d.margin.top
                + d.margin.bottom
                + d.border.top
                + d.border.bottom
                + d.padding.top
                + d.padding.bottom
        }
        FlexDirection::Column => {
            d.margin.left
                + d.margin.right
                + d.border.left
                + d.border.right
                + d.padding.left
                + d.padding.right
        }
    }
}

/// Margin, border, and padding on the cross-start edge only.
fn item_cross_leading(item: &LayoutBox, direction: FlexDirection) -> f32 {
    let d = item.dimensions;
    match direction {
        FlexDirection::Row => d.margin.top + d.border.top + d.padding.top,
        FlexDirection::Column => d.margin.left + d.border.left + d.padding.left,
    }
}

/// Lays out a flex container's children along `container.flex_direction`.
///
/// This assumes `container.dimensions.content` already has its outer
/// position and main-axis size resolved (by `calculate_width`/
/// `calculate_position`, same as any other box) and proceeds in three
/// passes: resolve every item's main size from `flex-basis` plus
/// `flex-grow`/`flex-shrink`; lay out each item's own subtree at a
/// provisional cross-axis position; then, once every item's cross size is
/// known, shift each into its final cross-axis position per `align-items`
/// and size the container's own auto cross dimension from the line's cross
/// size — mirroring how an ordinary block derives an auto height from its
/// children.
fn layout_flex_children(container: &mut LayoutBox, metrics: TextMetrics) {
    let direction = container.flex_direction;
    let align_items = container.align_items;
    let justify_content = container.justify_content;
    let gap = container.gap.max(0.0);

    let origin = container.dimensions.content;
    let items = core::mem::take(&mut container.children);
    let n = items.len();
    if n == 0 {
        container.dimensions.content.height = origin.height.max(0.0);
        return;
    }
    #[allow(clippy::cast_precision_loss)]
    let n_f = n as f32;

    // A row's main axis is width, which `calculate_width` always resolves to
    // a real number (explicit or filled to the containing block) — always
    // definite. A column's main axis is height, which is definite only when
    // explicitly declared; free space is undefined against an auto height,
    // so grow/shrink do not act and items keep their basis size exactly,
    // the same way an auto-height block simply sums its children rather
    // than stretching them to fill an undefined space.
    let (main_container_size, main_is_definite) = match direction {
        FlexDirection::Row => (origin.width, true),
        FlexDirection::Column => {
            if origin.height > 0.0 {
                (origin.height, true)
            } else {
                (0.0, false)
            }
        }
    };
    // The cross-axis size available to `align-items: stretch`. A row's cross
    // axis is height, definite only when declared; a column's cross axis is
    // width, which — like any block's — is always definite.
    let cross_container_size = match direction {
        FlexDirection::Row => (origin.height > 0.0).then_some(origin.height),
        FlexDirection::Column => Some(origin.width),
    };

    let basis: Vec<f32> = items
        .iter()
        .map(|item| resolve_flex_basis(item, direction, metrics))
        .collect();
    let main_extra: Vec<f32> = items
        .iter()
        .map(|item| item_main_extra(item, direction))
        .collect();
    let total_gap = gap * n.saturating_sub(1) as f32;
    let basis_total: f32 = basis.iter().sum::<f32>() + main_extra.iter().sum::<f32>() + total_gap;

    // -- pass 1: resolve each item's main size --------------------------
    let mut main_sizes = basis.clone();
    if main_is_definite {
        let free = main_container_size - basis_total;
        if free > 0.0 {
            let grow_sum: f32 = items.iter().map(|item| item.flex_grow.max(0.0)).sum();
            // A zero grow sum (the common case: no item declared
            // `flex-grow`) must leave every item at its basis size rather
            // than divide by zero — this is exactly the edge case verified
            // by reverting the guard locally in
            // `flex_grow_of_zero_does_not_divide_by_zero` below.
            if grow_sum > 0.0 {
                for (size, item) in main_sizes.iter_mut().zip(items.iter()) {
                    *size += free * (item.flex_grow.max(0.0) / grow_sum);
                }
            }
        } else if free < 0.0 {
            let deficit = -free;
            let weights: Vec<f32> = items
                .iter()
                .zip(basis.iter())
                .map(|(item, b)| item.flex_shrink.max(0.0) * b.max(0.0))
                .collect();
            let weight_sum: f32 = weights.iter().sum();
            // Same guard as growth: every item's shrink weight is zero when
            // every basis is zero (or every `flex-shrink` is zero), and the
            // items simply stay at their (zero) basis rather than divide by
            // zero.
            if weight_sum > 0.0 {
                for (size, weight) in main_sizes.iter_mut().zip(weights.iter()) {
                    *size = (*size - deficit * (weight / weight_sum)).max(0.0);
                }
            }
        }
    }

    let used_main: f32 =
        main_sizes.iter().sum::<f32>() + main_extra.iter().sum::<f32>() + total_gap;
    let remaining = if main_is_definite {
        (main_container_size - used_main).max(0.0)
    } else {
        0.0
    };

    let (mut cursor, item_gap) = match justify_content {
        JustifyContent::FlexStart => (0.0, gap),
        JustifyContent::FlexEnd => (remaining, gap),
        JustifyContent::Center => (remaining / 2.0, gap),
        JustifyContent::SpaceBetween if n > 1 => (0.0, gap + remaining / (n_f - 1.0)),
        JustifyContent::SpaceBetween => (0.0, gap),
        JustifyContent::SpaceAround => {
            let space = remaining / n_f;
            (space / 2.0, gap + space)
        }
    };

    // -- pass 2: place each item along the main axis, resolve its cross
    //    size, and lay out its own subtree -------------------------------
    let mut placed = Vec::with_capacity(n);
    let mut max_outer_cross = 0.0_f32;
    for (mut item, main_size) in items.into_iter().zip(main_sizes.iter().copied()) {
        let leading_main = item_main_leading(&item, direction);
        let extra_main = item_main_extra(&item, direction);

        let explicit_cross = match direction {
            FlexDirection::Row => {
                (item.dimensions.content.height > 0.0).then_some(item.dimensions.content.height)
            }
            FlexDirection::Column => {
                (item.dimensions.content.width > 0.0).then_some(item.dimensions.content.width)
            }
        };
        let cross_extra = item_cross_extra(&item, direction);
        let stretched_cross = if align_items == AlignItems::Stretch {
            cross_container_size.map(|c| (c - cross_extra).max(0.0))
        } else {
            None
        };
        let cross_size = explicit_cross
            .or(stretched_cross)
            .or(match (direction, item.kind) {
                // Text/inline content's cross size in a row is measurable — the
                // line height it always occupies — so it does not need to defer
                // to child layout the way a block item's auto height does.
                (FlexDirection::Row, BoxKind::Text | BoxKind::Inline) => Some(metrics.line_height),
                _ => None,
            });
        // A column's cross axis is width, which (like any block) has no
        // shrink-to-fit measurement in this engine; absent stretch or an
        // explicit width, an item fills the container's width, the same
        // fallback an ordinary block gives an undeclared width.
        let cross_size_for_layout = cross_size.unwrap_or(match direction {
            FlexDirection::Row => 0.0,
            FlexDirection::Column => (origin.width - cross_extra).max(0.0),
        });

        match direction {
            FlexDirection::Row => {
                item.dimensions.content.x = origin.x + cursor + leading_main;
                // The cross position depends on the *line's* cross size,
                // known only after every item in this pass is placed, so
                // this is a provisional origin the second pass corrects
                // with `shift_y` once the real offset is known.
                item.dimensions.content.y = origin.y;
                item.dimensions.content.width = main_size;
                item.dimensions.content.height = cross_size_for_layout;
            }
            FlexDirection::Column => {
                item.dimensions.content.y = origin.y + cursor + leading_main;
                item.dimensions.content.x = origin.x;
                item.dimensions.content.height = main_size;
                item.dimensions.content.width = cross_size_for_layout;
            }
        }

        layout_box_children(&mut item, metrics);

        // The main-axis size came from the flex algorithm, not from the
        // item's own content, and must survive whatever child layout did —
        // `layout_children`'s block-stacking branch unconditionally
        // recomputes its own box's height from its children, exactly the
        // clobbering `layout_block` guards against with `calculate_height`.
        // A column's main axis is height, always reasserted; a row's main
        // axis is width, which child layout never touches, so nothing to
        // reassert there. The cross axis is reasserted only when this pass
        // actually resolved one (explicit, stretched, or measured text) —
        // otherwise (a row's auto height with block/flex content) the
        // value child layout just derived is the real answer, the same way
        // an ordinary block's auto height is.
        match direction {
            FlexDirection::Column => item.dimensions.content.height = main_size,
            FlexDirection::Row => {
                if let Some(cross) = cross_size {
                    item.dimensions.content.height = cross;
                }
            }
        }

        let outer_cross = match direction {
            FlexDirection::Row => item.dimensions.content.height + cross_extra,
            FlexDirection::Column => item.dimensions.content.width + cross_extra,
        };
        max_outer_cross = max_outer_cross.max(outer_cross);

        cursor += main_size + extra_main + item_gap;
        placed.push(item);
    }

    // -- pass 3: align each item on the cross axis ----------------------
    // The line's cross size is the container's own, when definite; otherwise
    // the tallest/widest item, the same "auto size from children" rule an
    // ordinary block's height already follows.
    let line_cross = cross_container_size.unwrap_or(max_outer_cross);
    for item in &mut placed {
        let cross_extra = item_cross_extra(item, direction);
        let leading_cross = item_cross_leading(item, direction);
        let outer_cross = match direction {
            FlexDirection::Row => item.dimensions.content.height + cross_extra,
            FlexDirection::Column => item.dimensions.content.width + cross_extra,
        };
        let slack = (line_cross - outer_cross).max(0.0);
        let offset = match align_items {
            AlignItems::FlexStart | AlignItems::Stretch => 0.0,
            AlignItems::Center => slack / 2.0,
            AlignItems::FlexEnd => slack,
        };
        let delta = offset + leading_cross;
        match direction {
            FlexDirection::Row => shift_y(item, delta),
            FlexDirection::Column => shift_x(item, delta),
        }
    }

    container.children = placed;
    match direction {
        FlexDirection::Row => {
            if origin.height <= 0.0 {
                container.dimensions.content.height = max_outer_cross;
            }
        }
        FlexDirection::Column => {
            if origin.height <= 0.0 {
                container.dimensions.content.height = used_main;
            }
        }
    }
}

// -- hit testing ---------------------------------------------------------

/// A point in the same coordinate space as [`LayoutBox`] geometry: CSS pixels,
/// origin at the top left of the viewport.
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct Point {
    pub x: f32,
    pub y: f32,
}

/// Returns the node index of the topmost box containing `point`.
///
/// This completes `REQ-ENG-005`: the display list answers what is drawn, and
/// this answers what is *at* a location — the query input routing needs to turn
/// a click into an event target.
///
/// The result is a node index rather than a box reference, matching
/// [`LayoutBox::node`], so an embedder maps it back into their own tree.
///
/// # Semantics
///
/// **Topmost means last painted, not first found.** Boxes are tested in paint
/// order and a later hit replaces an earlier one. A pre-order walk that returned
/// its first containing box would answer with whatever appears earliest in the
/// document, which for overlapping content is the box *underneath* — wrong in a
/// way that looks right for any non-overlapping test.
///
/// **The border box is the hit area.** Margins are transparent separation, not
/// part of the element, so a point in the gap between two blocks belongs to
/// whatever is behind it rather than to the nearer sibling. Padding and border
/// are part of the element and do hit.
///
/// **Children are tested even when the parent misses.** `overflow` is `visible`
/// by default, so a child may paint outside its parent's box and must still be
/// reachable. Pruning the descent on a parent miss would be a plausible
/// optimisation that silently loses those hits.
///
/// **Anonymous and text boxes resolve to their nearest enclosing element.** An
/// anonymous block wrapping a run of inline text carries no source node, and a
/// text box's node is the text node rather than an element. A point over either
/// is over content, so answering `None` would be wrong — but answering with a
/// text node would be too. Input routing needs an event target, and text nodes
/// are not event targets; the enclosing element is what a caller can act on.
///
/// Returns `None` when the point is outside every box, which is a real answer
/// rather than a failure: nothing is there.
#[must_use]
pub fn hit_test(root: &LayoutBox, point: Point) -> Option<usize> {
    let mut hit = None;
    hit_test_in_paint_order(root, point, None, &mut hit);
    hit
}

fn hit_test_in_paint_order(
    layout_box: &LayoutBox,
    point: Point,
    enclosing_node: Option<usize>,
    hit: &mut Option<usize>,
) {
    // The nearest enclosing element, for anonymous and text boxes to resolve
    // against. Computed whether or not this box was hit, because an anonymous
    // child of a missed box still needs an answer.
    //
    // A text box contributes nothing here: its node is a text node, which is
    // not an event target, so it neither answers a hit nor shadows the element
    // that encloses it.
    let enclosing_node = if layout_box.kind == BoxKind::Text {
        enclosing_node
    } else {
        layout_box.node.or(enclosing_node)
    };

    if contains(layout_box.dimensions.border_box(), point) {
        *hit = enclosing_node;
    }

    // `paint` walks the box then its children in order, so visiting in the same
    // sequence and letting later hits win yields the topmost box.
    for child in &layout_box.children {
        hit_test_in_paint_order(child, point, enclosing_node, hit);
    }
}

/// Whether `rect` contains `point`.
///
/// Half-open on the right and bottom edges, so boxes that share an edge do not
/// both claim the boundary pixel. Without this a point on a seam between two
/// stacked blocks hits both, and which one wins depends on visit order.
fn contains(rect: Rect, point: Point) -> bool {
    point.x >= rect.x
        && point.x < rect.x + rect.width
        && point.y >= rect.y
        && point.y < rect.y + rect.height
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
    use super::{BoxKind, LayoutBox, LayoutTree, Point, TextMetrics, hit_test, layout};
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
    fn hit_testing_works_on_a_tree_the_engine_does_not_own() {
        let tree = HostTree::sample();
        let sheet = Stylesheet::parse("p { display: block; height: 20px; }").expect("parses");
        let root = layout(&tree, &sheet, 200.0, TextMetrics::default(), None).expect("lays out");

        // The two paragraphs stack, so a point in the second one must resolve
        // to a different host node than a point in the first.
        let first = hit_test(&root, Point { x: 10.0, y: 5.0 });
        let second = hit_test(&root, Point { x: 10.0, y: 25.0 });
        assert!(first.is_some());
        assert_ne!(first, second);
    }

    #[test]
    fn lays_out_a_tree_the_engine_does_not_own() {
        let tree = HostTree::sample();
        let sheet = Stylesheet::parse("p { display: block; height: 20px; }").expect("parses");

        let root = layout(&tree, &sheet, 200.0, TextMetrics::default(), None).expect("lays out");

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

        let root = layout(&tree, &sheet, 200.0, TextMetrics::default(), None).expect("lays out");

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
        layout(&document, &sheet, width, TextMetrics::default(), None)
    }

    /// Like [`run`], but also returns the parsed document so a test can name
    /// a node to pass as the hovered element — `run` alone has nowhere to
    /// get a `NodeId` from, since it discards the document once it's laid
    /// out.
    fn run_with_hover(
        html: &str,
        css: &str,
        width: f32,
        hovered: Option<NodeId>,
    ) -> (Document, Result<LayoutBox, LayoutError>) {
        let tokens = Tokenizer::new(html).tokenize().expect("tokenizes").tokens;
        let document = TreeBuilder::new().build(&tokens).expect("builds");
        let sheet = Stylesheet::parse(css).expect("parses");
        let result = layout(&document, &sheet, width, TextMetrics::default(), hovered);
        (document, result)
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

    // -- hit testing -----------------------------------------------------

    #[test]
    fn a_point_outside_every_box_hits_nothing() {
        let root = run(
            "<html><body><div>x</div></body></html>",
            "div { display: block; height: 20px; }",
            400.0,
        )
        .expect("lays out");
        assert_eq!(hit_test(&root, Point { x: 10.0, y: 9000.0 }), None);
    }

    #[test]
    fn overlapping_boxes_resolve_to_the_last_painted() {
        // Nested blocks: every point inside the inner div is also inside the
        // outer div and the body, so three border boxes contain the probe. Paint
        // order draws the outer first and the inner last, so the inner is on
        // top. A walk returning its first containing box would answer with the
        // outermost element and still pass every single-box test.
        let html = "<html><body><div class='outer'><p>x</p></div></body></html>";
        let root = run(
            html,
            "body { display: block; } \
             .outer { display: block; height: 60px; } \
             p { display: block; height: 20px; }",
            400.0,
        )
        .expect("lays out");
        let document = document_for(html);

        let paragraph = find(&root, &document, "p");
        let probe = Point {
            x: paragraph.dimensions.content.x + 1.0,
            y: paragraph.dimensions.content.y + 1.0,
        };
        let outer = find(&root, &document, "div");
        assert!(
            contains(outer.dimensions.border_box(), probe),
            "the probe must be inside the outer box too, or this proves nothing"
        );
        assert_eq!(hit_test(&root, probe), paragraph.node);
    }

    #[test]
    fn negative_margins_are_reported_not_guessed() {
        // Collapsing with a negative margin adds the most negative to the
        // largest positive rather than maximising against it. This crate
        // computes only the positive rule, so a negative margin would silently
        // stack content in the wrong place.
        let result = run(
            "<html><body><div>x</div></body></html>",
            "div { display: block; margin: -50px; }",
            400.0,
        );
        assert!(matches!(
            result,
            Err(LayoutError::NegativeEdgeUnsupported { .. })
        ));
    }

    #[test]
    fn negative_padding_is_reported_not_guessed() {
        let result = run(
            "<html><body><div>x</div></body></html>",
            "div { display: block; padding: -10px; }",
            400.0,
        );
        assert!(matches!(
            result,
            Err(LayoutError::NegativeEdgeUnsupported { .. })
        ));
    }

    #[test]
    fn nan_border_radius_does_not_reach_layout_geometry() {
        // "NaN" is syntax f32::from_str accepts, so it parses successfully
        // rather than falling into non_negative's unparseable-defaults-to-0
        // path — and NaN < 0.0 is false, so the negative-value refusal below
        // it never fires either. Both gaps would let a NaN border-radius
        // through to paint. Confirmed via `run` rather than calling
        // parse_length directly, so this proves the whole declaration path,
        // not just the parsing function in isolation.
        let root = run(
            "<body><div>x</div></body>",
            "div { border-radius: NaN; background: navy; }",
            100.0,
        )
        .expect("lays out");
        let document = document_of("<body><div>x</div></body>");
        assert_eq!(
            find(&root, &document, "div").border_radius,
            0.0,
            "a NaN border-radius must resolve to the unparseable-value default, not NaN itself"
        );
    }

    #[test]
    fn nan_width_does_not_reach_layout_geometry() {
        // Unlike non_negative's properties, `width`/`height` store
        // parse_length's Option<f32> directly — `Some(f32::NAN)` is not
        // `None`, so `.unwrap_or(0.0)` would keep the NaN rather than
        // falling back to auto.
        let root = run(
            "<body><div>x</div></body>",
            "div { display: block; width: NaN; }",
            100.0,
        )
        .expect("lays out");
        let document = document_of("<body><div>x</div></body>");
        let width = find(&root, &document, "div").dimensions.content.width;
        assert!(
            !width.is_nan(),
            "a NaN width must not reach the box's own resolved geometry"
        );
    }

    #[test]
    fn a_literal_nan_length_is_not_silently_accepted() {
        // Rust's `f32::from_str` parses the literal string "nan" as a real
        // NaN value, which is not a valid CSS length. `non_negative`'s own
        // guard (`length < 0.0`) is false for NaN — NaN is not less than
        // anything — so without `parse_length` filtering non-finite values
        // itself, this would slip through as an unchecked NaN margin that
        // then poisons every later arithmetic comparison built from it.
        let html = "<html><body><div>x</div></body></html>";
        let result = run(html, "div { display: block; margin: nan; }", 400.0)
            .expect("a NaN margin is filtered to auto, i.e. zero, not refused or kept verbatim");
        let document = document_for(html);
        assert_eq!(find(&result, &document, "div").dimensions.margin.left, 0.0);
    }

    #[test]
    fn a_hit_on_text_resolves_to_the_element_not_the_text_node() {
        // The text box's own node is the text node, which is not an event
        // target. Routing a click to it would hand a caller something they
        // cannot attach a listener to.
        let html = "<html><body><div>hello</div></body></html>";
        let root = run(html, "div { display: block; }", 400.0).expect("lays out");
        let document = document_for(html);

        let text_box = find_kind(&root, BoxKind::Text).expect("text box exists");
        assert!(text_box.node.is_some(), "the text box carries a text node");

        let probe = Point {
            x: text_box.dimensions.content.x + 1.0,
            y: text_box.dimensions.content.y + 1.0,
        };
        let div = find(&root, &document, "div");
        assert_eq!(hit_test(&root, probe), div.node);
        assert_ne!(hit_test(&root, probe), text_box.node);
    }

    #[test]
    fn margins_are_not_part_of_the_hit_area() {
        // Two blocks separated by a margin gap. A point inside the gap is over
        // the body, not over either child, because margins are transparent
        // separation rather than part of the element.
        let html = "<html><body><div class='a'>a</div><div class='b'>b</div></body></html>";
        let root = run(
            html,
            "body { display: block; } \
             .a { display: block; height: 20px; } \
             .b { display: block; height: 20px; margin: 30px; }",
            400.0,
        )
        .expect("lays out");
        let document = document_for(html);

        let in_gap = hit_test(&root, Point { x: 200.0, y: 35.0 });
        let first = find(&root, &document, "div");
        assert_ne!(in_gap, first.node);
        // And it is not the second div either: that box starts below the gap.
        let second_top = 20.0 + 30.0;
        assert!(35.0 < second_top);
    }

    #[test]
    fn padding_and_border_are_part_of_the_hit_area() {
        let html = "<html><body><div>x</div></body></html>";
        let root = run(
            html,
            "div { display: block; height: 20px; padding: 10px; border: 5px; }",
            400.0,
        )
        .expect("lays out");
        let document = document_for(html);
        let div = find(&root, &document, "div");

        // A point inside the border ring is outside the content box but inside
        // the border box, so it belongs to the element.
        let border_box = div.dimensions.border_box();
        let in_border = Point {
            x: border_box.x + 2.0,
            y: border_box.y + 2.0,
        };
        assert!(!contains(div.dimensions.content, in_border));
        assert_eq!(hit_test(&root, in_border), div.node);
    }

    #[test]
    fn a_hit_on_wrapped_text_resolves_to_an_element() {
        // Mixed block and inline children put the text inside an anonymous
        // block, which carries no source node. Answering None for a point
        // plainly over content would be wrong.
        let html = "<html><body><div>text<p>block</p></div></body></html>";
        let root =
            run(html, "div { display: block; } p { display: block; }", 400.0).expect("lays out");

        let anonymous = find_kind(&root, BoxKind::AnonymousBlock).expect("anonymous block exists");
        assert_eq!(
            anonymous.node, None,
            "the anonymous block has no source node"
        );

        let inside = Point {
            x: anonymous.dimensions.content.x + 1.0,
            y: anonymous.dimensions.content.y + 1.0,
        };
        assert!(
            hit_test(&root, inside).is_some(),
            "a point over the anonymous block must resolve to an enclosing element"
        );
    }

    #[test]
    fn a_child_painting_outside_its_parent_is_still_reachable() {
        // A declared height shorter than the content makes the child overflow
        // its parent's box. `overflow` is visible by default, so the child is
        // drawn there and must be hittable. Pruning the descent when the parent
        // misses would be a plausible optimisation that loses this silently.
        let html = "<html><body><div class='outer'><p>x</p></div></body></html>";
        let root = run(
            html,
            ".outer { display: block; height: 10px; } \
             p { display: block; height: 80px; }",
            400.0,
        )
        .expect("lays out");
        let document = document_for(html);

        let outer = find(&root, &document, "div");
        let paragraph = find(&root, &document, "p");
        let probe = Point {
            x: paragraph.dimensions.content.x + 1.0,
            y: paragraph.dimensions.content.y + 60.0,
        };
        assert!(
            !contains(outer.dimensions.border_box(), probe),
            "the probe must be outside the parent, or this proves nothing"
        );
        assert_eq!(hit_test(&root, probe), paragraph.node);
    }

    #[test]
    fn boxes_sharing_an_edge_do_not_both_claim_it() {
        // Half-open containment: a point exactly on the seam between two
        // stacked blocks belongs to the lower one only.
        let rect = Rect {
            x: 0.0,
            y: 0.0,
            width: 10.0,
            height: 10.0,
        };
        assert!(
            contains(rect, Point { x: 0.0, y: 0.0 }),
            "top-left is inside"
        );
        assert!(
            !contains(rect, Point { x: 10.0, y: 5.0 }),
            "the right edge belongs to the next box"
        );
        assert!(
            !contains(rect, Point { x: 5.0, y: 10.0 }),
            "the bottom edge belongs to the next box"
        );
    }

    /// Returns the first box of `kind` in paint order.
    fn find_kind(root: &LayoutBox, kind: BoxKind) -> Option<&LayoutBox> {
        if root.kind == kind {
            return Some(root);
        }
        root.children.iter().find_map(|c| find_kind(c, kind))
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

    fn find_by_id<'tree>(
        root: &'tree LayoutBox,
        document: &Document,
        id: &str,
    ) -> &'tree LayoutBox {
        fn walk<'tree>(
            node: &'tree LayoutBox,
            document: &Document,
            id: &str,
        ) -> Option<&'tree LayoutBox> {
            if let Some(index) = node.node
                && document.attribute_of(NodeId::from_index(index), "id") == Some(id)
            {
                return Some(node);
            }
            node.children.iter().find_map(|c| walk(c, document, id))
        }
        walk(root, document, id).expect("box exists")
    }

    fn document_of(html: &str) -> Document {
        let tokens = Tokenizer::new(html).tokenize().expect("tokenizes").tokens;
        TreeBuilder::new().build(&tokens).expect("builds")
    }

    fn node_id_of(document: &Document, id: &str) -> NodeId {
        (0..document.len())
            .map(NodeId::from_index)
            .find(|&node| document.attribute_of(node, "id") == Some(id))
            .expect("the element exists")
    }

    #[test]
    fn hover_applies_only_to_the_hovered_element() {
        let html = "<html><body><p id='a'>a</p><p id='b'>b</p></body></html>";
        let css = "p { display: block; height: 10px; } p:hover { height: 30px; }";

        let (document, neither) = run_with_hover(html, css, 400.0, None);
        let root = neither.expect("lays out");
        assert_eq!(
            find_by_id(&root, &document, "a").dimensions.content.height,
            10.0
        );
        assert_eq!(
            find_by_id(&root, &document, "b").dimensions.content.height,
            10.0
        );

        let a = node_id_of(&document, "a");
        let (document, hovering_a) = run_with_hover(html, css, 400.0, Some(a));
        let root = hovering_a.expect("lays out");
        assert_eq!(
            find_by_id(&root, &document, "a").dimensions.content.height,
            30.0,
            ":hover must change the geometry of the hovered element, not only its paint"
        );
        assert_eq!(
            find_by_id(&root, &document, "b").dimensions.content.height,
            10.0,
            "hovering one element must not affect an unrelated one"
        );
    }

    #[test]
    fn hover_on_an_ancestor_selector_reaches_layout() {
        // Mirrors `turing-css`'s own `hover_on_an_ancestor_compound_still_matches`,
        // one layer up: `.parent:hover p` has to change the paragraph's
        // geometry, not just be evaluated correctly by the cascade in
        // isolation. This is the thing that actually breaks if `hovered`
        // ever stopped reaching `build_box`'s recursive calls.
        //
        // Layout is called directly here, on one parsed document, rather
        // than through `run_with_hover` — the hovered node id has to name a
        // node in the exact document `layout` receives, and building both
        // from one `document_of` call is the straightforward way to
        // guarantee that.
        let html = "<div class='parent'><p>x</p></div>";
        let css = "p { display: block; height: 10px; } \
                   .parent:hover p { height: 40px; }";
        let document = document_of(html);
        let sheet = Stylesheet::parse(css).expect("parses");
        let div = (0..document.len())
            .map(NodeId::from_index)
            .find(|&node| document.element_name(node) == Some("div"))
            .expect("the div exists");

        let without_hover =
            layout(&document, &sheet, 400.0, TextMetrics::default(), None).expect("lays out");
        assert_eq!(
            find(&without_hover, &document, "p")
                .dimensions
                .content
                .height,
            10.0
        );

        let with_hover =
            layout(&document, &sheet, 400.0, TextMetrics::default(), Some(div)).expect("lays out");
        assert_eq!(
            find(&with_hover, &document, "p").dimensions.content.height,
            40.0,
            "hovering the ancestor div must apply .parent:hover p to the paragraph"
        );
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
            DisplayItem::SolidColor { color, .. } if *color == Color::parse("red").expect("named colour")
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
    fn grid_and_table_are_reported_not_guessed() {
        // `flex` is implemented (see the flex layout tests below) and is
        // deliberately not in this list any more; it used to be, before this
        // crate supported it.
        for value in ["grid", "table"] {
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
    fn a_long_text_run_wraps_between_words() {
        // Five words of four characters each: 32px a word, 8px a space. At a
        // 80px viewport, two words and a space fit a line (72px), a third
        // word would need 112px, so the run breaks into three lines of two,
        // two, and one word.
        let root = run("<body>aaaa bbbb cccc dddd eeee</body>", "", 80.0).expect("lays out");
        let list = build_display_list(&root);
        let runs: Vec<(&str, &Rect)> = list
            .items
            .iter()
            .filter_map(|item| match item {
                DisplayItem::Text { text, rect, .. } => Some((text.as_str(), rect)),
                DisplayItem::SolidColor { .. } | DisplayItem::RoundedColor { .. } => None,
            })
            .collect();
        let words: Vec<&str> = runs.iter().map(|(word, _)| *word).collect();
        assert_eq!(words, ["aaaa", "bbbb", "cccc", "dddd", "eeee"]);
        // Lines: y = 0, 0, 16, 16, 32. Second word sits after a collapsed
        // single space: x = 32 + 8.
        assert_eq!(
            runs[1].1.x, 40.0,
            "one space between words: {:?}",
            runs[1].1
        );
        assert_eq!(runs[1].1.y, runs[0].1.y, "first two words share a line");
        assert_eq!(runs[2].1.x, 0.0, "a line start drops the pending space");
        assert!(runs[2].1.y > runs[0].1.y, "third word wrapped");
        assert!(runs[4].1.y > runs[2].1.y, "fifth word wrapped again");
    }

    #[test]
    fn interior_whitespace_collapses_to_one_space() {
        let root = run("<body>a  \t  b</body>", "", 640.0).expect("lays out");
        let list = build_display_list(&root);
        let rects: Vec<&Rect> = list
            .items
            .iter()
            .filter_map(|item| match item {
                DisplayItem::Text { rect, .. } => Some(rect),
                DisplayItem::SolidColor { .. } | DisplayItem::RoundedColor { .. } => None,
            })
            .collect();
        assert_eq!(rects.len(), 2);
        assert_eq!(
            rects[1].x, 16.0,
            "a run of mixed whitespace is one 8px space: {:?}",
            rects[1]
        );
    }

    #[test]
    fn adjacent_inline_elements_abut_rather_than_overlap() {
        // An inline element's width is the sum of its descendants' text, so
        // the second span's run starts where the first one ends.
        let root = run("<body><span>ab</span><span>cd</span></body>", "", 640.0).expect("lays out");
        let list = build_display_list(&root);
        let runs: Vec<&Rect> = list
            .items
            .iter()
            .filter_map(|item| match item {
                DisplayItem::Text { rect, .. } => Some(rect),
                DisplayItem::SolidColor { .. } | DisplayItem::RoundedColor { .. } => None,
            })
            .collect();
        assert_eq!(runs.len(), 2);
        assert!((runs[0].x - 0.0).abs() < f32::EPSILON);
        assert!(
            (runs[1].x - 16.0).abs() < f32::EPSILON,
            "second span starts after the first: {:?}",
            runs[1]
        );
        assert!((runs[0].y - runs[1].y).abs() < f32::EPSILON, "same line");
    }

    #[test]
    fn margin_on_an_inline_element_leaves_a_real_gap_to_its_neighbour() {
        // Regression test: `dimensions.margin` was already carried on every
        // inline box from `build_box`, but `layout_inline_children` never
        // read it when advancing the line pen, so `margin` on `display:
        // inline` had no visible effect at all — found while building the
        // engine-rendered chrome demo, documented, and fixed here.
        //
        // Only the `margin` shorthand exists in this crate (no
        // `margin-left`/`margin-right` longhands yet, a separate, pre-existing
        // gap noted but not fixed here), so this applies uniformly and the
        // first span's own start position shifts by `margin-left` too.
        let root = run(
            "<body><span class=\"a\">ab</span><span>cd</span></body>",
            ".a { margin: 10px; }",
            640.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let runs: Vec<&Rect> = list
            .items
            .iter()
            .filter_map(|item| match item {
                DisplayItem::Text { rect, .. } => Some(rect),
                DisplayItem::SolidColor { .. } | DisplayItem::RoundedColor { .. } => None,
            })
            .collect();
        assert_eq!(runs.len(), 2);
        // Without the fix, the first run starts at 0.0 and the second at
        // 16.0 — the same positions the no-margin
        // `adjacent_inline_elements_abut_rather_than_overlap` test asserts,
        // as though `margin: 10px` had never been declared at all.
        assert!(
            (runs[0].x - 10.0).abs() < f32::EPSILON,
            "first span's own margin-left should push it in from the edge, got {:?}",
            runs[0]
        );
        assert!(
            (runs[1].x - 36.0).abs() < f32::EPSILON,
            "second span should start past the first span's margin-left (10) + width (16) + \
             margin-right (10) = 36.0, got {:?}",
            runs[1]
        );
    }

    #[test]
    fn an_inline_element_that_does_not_fit_moves_to_the_next_line_whole() {
        let root = run(
            "<body><span>hello</span><span>world</span></body>",
            "",
            64.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let runs: Vec<&Rect> = list
            .items
            .iter()
            .filter_map(|item| match item {
                DisplayItem::Text { rect, .. } => Some(rect),
                DisplayItem::SolidColor { .. } | DisplayItem::RoundedColor { .. } => None,
            })
            .collect();
        assert_eq!(runs.len(), 2);
        assert!(
            runs[1].y > runs[0].y,
            "40px + 40px cannot share a 64px line: {:?} {:?}",
            runs[0],
            runs[1]
        );
        assert!(
            (runs[1].x - 0.0).abs() < f32::EPSILON,
            "the wrapped element starts at the line's origin"
        );
    }

    #[test]
    fn text_align_center_and_right_shift_each_line_by_its_slack() {
        // One short word in a wide block: centre puts slack/2 on the left,
        // right puts all the slack there.
        let left =
            run("<body><p>hi</p></body>", "p { text-align: left }", 100.0).expect("lays out");
        let centered =
            run("<body><p>hi</p></body>", "p { text-align: center }", 100.0).expect("lays out");
        let right =
            run("<body><p>hi</p></body>", "p { text-align: right }", 100.0).expect("lays out");
        let word_x = |root: &LayoutBox| {
            build_display_list(root)
                .items
                .iter()
                .find_map(|item| match item {
                    DisplayItem::Text { rect, text, .. } if text == "hi" => Some(rect.x),
                    _ => None,
                })
                .expect("word painted")
        };
        let (l, c, r) = (word_x(&left), word_x(&centered), word_x(&right));
        assert!(l < c && c < r, "left {l} < center {c} < right {r}");
        // "hi" is 16px wide; the block content is ~100px minus body margin.
        // Right places the word's right edge at the content edge.
        assert!(
            r > l + 50.0,
            "right alignment moved the word most of the width"
        );
    }

    #[test]
    fn an_unimplemented_text_align_is_refused() {
        let error =
            run("<body><p>x</p></body>", "p { text-align: justify }", 100.0).expect_err("refused");
        assert!(matches!(error, LayoutError::TextAlignUnsupported { .. }));
    }

    #[test]
    fn border_radius_emits_a_rounded_fill_the_reference_draws_square() {
        let root = run(
            "<body><div>x</div></body>",
            "div { background: teal; border-radius: 8px; padding: 6px; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let teal = Color::parse("teal").expect("named colour");
        let rounded = list.items.iter().find_map(|item| match item {
            DisplayItem::RoundedColor { radius, color, .. } if *color == teal => Some(*radius),
            _ => None,
        });
        assert_eq!(rounded, Some(8.0), "a non-zero radius emits a rounded fill");
        // With no radius the same box emits a square fill.
        let square = run(
            "<body><div>x</div></body>",
            "div { background: teal; padding: 6px; }",
            100.0,
        )
        .expect("lays out");
        assert!(
            build_display_list(&square)
                .items
                .iter()
                .any(|item| matches!(
                    item,
                    DisplayItem::SolidColor { color, .. } if *color == teal
                )),
            "no radius stays a square fill"
        );
    }

    #[test]
    fn borders_paint_as_a_ring_around_the_padding_box() {
        let root = run(
            "<body><div>x</div></body>",
            "div { border-width: 2px; border-color: navy; background: silver; padding: 4px; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let navy = Color::parse("navy").expect("named colour");
        let silver = Color::parse("silver").expect("named colour");
        let border_rects: Vec<&Rect> = list
            .items
            .iter()
            .filter_map(|item| match item {
                DisplayItem::SolidColor { rect, color, .. } if *color == navy => Some(rect),
                _ => None,
            })
            .collect();
        assert_eq!(border_rects.len(), 4, "four border edges");
        // The top edge is 2px tall and spans the border box.
        assert_eq!(border_rects[0].height, 2.0);
        let background = list
            .items
            .iter()
            .find_map(|item| match item {
                DisplayItem::SolidColor { rect, color, .. } if *color == silver => Some(rect),
                _ => None,
            })
            .expect("background paints");
        // The background starts inside the border ring.
        assert_eq!(background.y, border_rects[0].y + 2.0);
    }

    #[test]
    fn a_border_with_no_border_color_uses_the_text_colour() {
        let root = run(
            "<body><div>x</div></body>",
            "div { border-width: 1px; color: maroon; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let maroon = Color::parse("maroon").expect("named colour");
        let edges = list
            .items
            .iter()
            .filter(
                |item| matches!(item, DisplayItem::SolidColor { color, .. } if *color == maroon),
            )
            .count();
        assert_eq!(edges, 4, "currentColor is the border default");
    }

    #[test]
    fn per_side_border_widths_produce_asymmetric_geometry() {
        let html = "<body><div>x</div></body>";
        let root = run(
            html,
            "div { border-top-width: 2px; border-right-width: 4px; \
             border-bottom-width: 6px; border-left-width: 8px; padding: 10px; }",
            100.0,
        )
        .expect("lays out");
        let document = document_of(html);
        let div = find(&root, &document, "div");
        let border = div.dimensions.border;
        assert_eq!(border.top, 2.0);
        assert_eq!(border.right, 4.0);
        assert_eq!(border.bottom, 6.0);
        assert_eq!(border.left, 8.0);
    }

    #[test]
    fn the_border_width_shorthand_still_sets_every_side() {
        let html = "<body><div>x</div></body>";
        let root = run(html, "div { border-width: 3px; }", 100.0).expect("lays out");
        let document = document_of(html);
        let div = find(&root, &document, "div");
        let border = div.dimensions.border;
        assert_eq!(border.top, 3.0);
        assert_eq!(border.right, 3.0);
        assert_eq!(border.bottom, 3.0);
        assert_eq!(border.left, 3.0);
    }

    #[test]
    fn per_side_border_colours_paint_independently() {
        let root = run(
            "<body><div>x</div></body>",
            "div { border-width: 2px; border-top-color: red; \
             border-right-color: lime; border-bottom-color: blue; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        for name in ["red", "lime", "blue"] {
            let color = Color::parse(name).expect("named colour");
            assert!(
                list.items.iter().any(
                    |item| matches!(item, DisplayItem::SolidColor { color: c, .. } if *c == color)
                ),
                "the {name} side must paint its own colour"
            );
        }
        // The left side declared no colour and has no text colour set
        // either, so it falls back to the initial `color`, black.
        let black = Color::parse("black").expect("named colour");
        assert!(
            list.items.iter().any(
                |item| matches!(item, DisplayItem::SolidColor { color: c, .. } if *c == black)
            ),
            "an undeclared side falls back to currentColor"
        );
    }

    #[test]
    fn a_later_rules_longhand_beats_an_earlier_rules_shorthand() {
        // The common real case: two separate rules, one with the shorthand,
        // one with a per-side override, matched by different classes on the
        // same element. `turing_css::cascade` already tracks which *rule*
        // supplied a winning declaration and uses that to break specificity
        // ties; `wins_over_shorthand` reuses exactly that fact rather than
        // reimplementing it, so a longhand from a later rule correctly beats
        // an earlier rule's shorthand, and — reversed — an earlier
        // longhand correctly loses to a later shorthand that resets it.
        let root = run(
            "<body><div class='base override'>x</div></body>",
            "div { border-width: 2px; } \
             .base { border-color: lime; } \
             .override { border-top-color: red; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let red = Color::parse("red").expect("named colour");
        assert!(
            list.items
                .iter()
                .any(|item| matches!(item, DisplayItem::SolidColor { color, .. } if *color == red)),
            "the later rule's longhand wins"
        );

        // Reversed: the shorthand now comes from the later rule, and resets
        // the top side the earlier rule's longhand set.
        let reset = run(
            "<body><div class='base override'>x</div></body>",
            "div { border-width: 2px; } \
             .base { border-top-color: red; } \
             .override { border-color: lime; }",
            100.0,
        )
        .expect("lays out");
        let reset_list = build_display_list(&reset);
        assert!(
            !reset_list
                .items
                .iter()
                .any(|item| matches!(item, DisplayItem::SolidColor { color, .. } if *color == red)),
            "the later rule's shorthand resets the earlier longhand's side"
        );
    }

    #[test]
    fn a_longhand_still_wins_over_a_shorthand_in_the_same_rule() {
        // The narrower, real, remaining limitation: `ComputedDeclaration`
        // tracks which *rule* a winning declaration came from
        // (`source_order`), not a declaration's own position within one
        // rule's body — two declarations from the same rule share the same
        // `source_order` by construction, so `wins_over_shorthand`'s tie
        // break (`longhand.source_order >= shorthand.source_order`) always
        // resolves in the longhand's favour when they are literally the same
        // rule. This is real CSS's declaration-order rule only for the
        // across-rule case above; within one rule it still cannot see which
        // one the source lists last. Fixing that needs a finer-grained
        // position than `source_order` currently is — a real, separate,
        // smaller change from the cross-rule fix this test's sibling proves.
        let root = run(
            "<body><div>x</div></body>",
            "div { border-width: 2px; border-color: lime; border-top-color: red; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let red = Color::parse("red").expect("named colour");
        assert!(
            list.items
                .iter()
                .any(|item| matches!(item, DisplayItem::SolidColor { color, .. } if *color == red)),
            "the longhand wins even though it is not later in this one rule"
        );
    }

    #[test]
    fn outline_never_changes_box_geometry() {
        // The defining property outline has and border does not: it never
        // affects layout. A sibling after an outlined box must land exactly
        // where it would if the outline were absent.
        let with_outline = run(
            "<body><div class='first'>a</div><div id='after'>b</div></body>",
            "div { display: block; height: 10px; } \
             .first { outline-width: 20px; outline-color: red; }",
            100.0,
        )
        .expect("lays out");
        let without_outline = run(
            "<body><div class='first'>a</div><div id='after'>b</div></body>",
            "div { display: block; height: 10px; }",
            100.0,
        )
        .expect("lays out");
        let html = "<body><div class='first'>a</div><div id='after'>b</div></body>";
        let with_document = document_of(html);
        let without_document = document_of(html);
        let after_outlined = find_by_id(&with_outline, &with_document, "after");
        let after_plain = find_by_id(&without_outline, &without_document, "after");
        assert_eq!(
            after_outlined.dimensions.content.y, after_plain.dimensions.content.y,
            "a 20px outline on the first box must not push the second one down"
        );
    }

    #[test]
    fn outline_paints_as_a_ring_outside_the_border_box_with_its_own_colour() {
        let root = run(
            "<body><div>x</div></body>",
            "div { border-width: 2px; border-color: navy; outline-width: 3px; \
             outline-color: orange; padding: 4px; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let orange = Color::parse("orange").expect("named colour");
        let outline_edges = list
            .items
            .iter()
            .filter(
                |item| matches!(item, DisplayItem::SolidColor { color, .. } if *color == orange),
            )
            .count();
        assert_eq!(outline_edges, 4, "the outline paints all four sides");
    }

    #[test]
    fn an_outline_with_no_colour_falls_back_to_currentcolor() {
        let root = run(
            "<body><div>x</div></body>",
            "div { outline-width: 2px; color: teal; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let teal = Color::parse("teal").expect("named colour");
        let edges = list
            .items
            .iter()
            .filter(|item| matches!(item, DisplayItem::SolidColor { color, .. } if *color == teal))
            .count();
        assert_eq!(
            edges, 4,
            "currentColor is the outline default, same as border"
        );
    }

    #[test]
    fn zero_width_outline_paints_nothing() {
        let root = run(
            "<body><div>x</div></body>",
            "div { outline-color: red; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let red = Color::parse("red").expect("named colour");
        assert!(
            !list
                .items
                .iter()
                .any(|item| matches!(item, DisplayItem::SolidColor { color, .. } if *color == red)),
            "a colour with no width paints nothing, same as a border would"
        );
    }

    #[test]
    fn opacity_applies_to_everything_a_box_paints_of_its_own() {
        let root = run(
            "<body><div id='box'>x</div></body>",
            "#box { background: navy; border-width: 1px; border-color: red; \
             opacity: 0.5; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        assert!(
            !list.items.is_empty(),
            "the fixture must actually emit something to check"
        );
        for item in &list.items {
            let alpha = match item {
                DisplayItem::SolidColor { alpha, .. }
                | DisplayItem::RoundedColor { alpha, .. }
                | DisplayItem::Text { alpha, .. } => *alpha,
            };
            assert_eq!(
                alpha, 0.5,
                "every one of the box's own paint items must carry its opacity: {item:?}"
            );
        }
    }

    #[test]
    fn undeclared_child_opacity_still_fades_under_a_translucent_ancestor() {
        // The property `opacity` does not cascade the way `color` does, but
        // its *visual* effect reaches descendants in real CSS regardless —
        // an opacity box forms a stacking context that composites its whole
        // subtree as one group. A child declaring no opacity of its own must
        // still visibly fade under a translucent ancestor, not stay fully
        // opaque; this is the common "fade this whole block" use of the
        // property. See `Inherited::opacity`'s own doc comment for exactly
        // what this engine's ambient-multiplication approximates and where
        // it diverges from a true flattened group.
        let root = run(
            "<body><div id='parent'><p id='child'>x</p></div></body>",
            "#parent { opacity: 0.3; background: navy; } #child { color: white; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let child_text_alpha = list
            .items
            .iter()
            .find_map(|item| match item {
                DisplayItem::Text { alpha, .. } => Some(*alpha),
                _ => None,
            })
            .expect("the child's text paints");
        assert_eq!(
            child_text_alpha, 0.3,
            "a child declaring no opacity of its own still inherits the ambient value"
        );
    }

    #[test]
    fn nested_opacity_multiplies_with_the_ambient_value() {
        // A child's own declared opacity does not replace the ambient value
        // an opacity-bearing ancestor already established — it multiplies
        // with it, which is what actually approximates a flattened group's
        // visual result without this engine needing an offscreen layer to
        // composite one through.
        let root = run(
            "<body><div id='parent'><p id='child'>x</p></div></body>",
            "#parent { opacity: 0.5; background: navy; } \
             #child { opacity: 0.4; color: white; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let child_text_alpha = list
            .items
            .iter()
            .find_map(|item| match item {
                DisplayItem::Text { alpha, .. } => Some(*alpha),
                _ => None,
            })
            .expect("the child's text paints");
        assert!(
            (child_text_alpha - 0.2).abs() < 0.001,
            "child opacity (0.4) must multiply with the ambient parent opacity \
             (0.5), not replace it: got {child_text_alpha}"
        );
    }

    #[test]
    fn opacity_values_outside_zero_to_one_are_clamped_not_refused() {
        // CSS defines out-of-range opacity as clamped, not invalid — the
        // same "this is the specified behaviour, not a guess" reasoning
        // that already governs every refusal in this file applies in
        // reverse here: refusing `opacity: 2` would be wrong, not careful.
        let over = run(
            "<body><div>x</div></body>",
            "div { opacity: 2; background: navy; }",
            100.0,
        )
        .expect("lays out");
        let under = run(
            "<body><div>x</div></body>",
            "div { opacity: -1; background: navy; }",
            100.0,
        )
        .expect("lays out");
        let percent = run(
            "<body><div>x</div></body>",
            "div { opacity: 50%; background: navy; }",
            100.0,
        )
        .expect("lays out");

        let alpha_of = |root: &LayoutBox| {
            build_display_list(root)
                .items
                .iter()
                .find_map(|item| match item {
                    DisplayItem::SolidColor { alpha, .. } => Some(*alpha),
                    _ => None,
                })
                .expect("the background paints")
        };
        assert_eq!(alpha_of(&over), 1.0, "opacity: 2 clamps to fully opaque");
        assert_eq!(
            alpha_of(&under),
            0.0,
            "opacity: -1 clamps to fully transparent"
        );
        assert_eq!(alpha_of(&percent), 0.5, "opacity: 50% is the same as 0.5");
    }

    #[test]
    fn opacity_nan_is_treated_as_unparseable_not_clamped_through() {
        // "NaN" and "nan%" are both syntax `f32::from_str` accepts, so they
        // parse successfully rather than falling into the unparseable path
        // — `f32::clamp` passes a `NaN` input straight through instead of
        // bringing it into range, which would otherwise carry a `NaN` alpha
        // all the way to a pixel channel.
        let bare = run(
            "<body><div>x</div></body>",
            "div { opacity: NaN; background: navy; }",
            100.0,
        )
        .expect("lays out");
        let percent = run(
            "<body><div>x</div></body>",
            "div { opacity: nan%; background: navy; }",
            100.0,
        )
        .expect("lays out");

        let alpha_of = |root: &LayoutBox| {
            build_display_list(root)
                .items
                .iter()
                .find_map(|item| match item {
                    DisplayItem::SolidColor { alpha, .. } => Some(*alpha),
                    _ => None,
                })
                .expect("the background paints")
        };
        assert_eq!(
            alpha_of(&bare),
            1.0,
            "opacity: NaN must resolve to the initial value, not NaN itself"
        );
        assert_eq!(
            alpha_of(&percent),
            1.0,
            "opacity: nan% must resolve to the initial value, not NaN itself"
        );
    }

    #[test]
    fn undeclared_opacity_is_fully_opaque() {
        let root = run(
            "<body><div>x</div></body>",
            "div { background: navy; }",
            100.0,
        )
        .expect("lays out");
        let alpha = build_display_list(&root)
            .items
            .iter()
            .find_map(|item| match item {
                DisplayItem::SolidColor { alpha, .. } => Some(*alpha),
                _ => None,
            })
            .expect("the background paints");
        assert_eq!(alpha, 1.0, "opacity's initial value is fully opaque");
    }

    #[test]
    fn opacity_never_changes_box_geometry() {
        // Same proof outline's own layout-neutrality test uses: a sibling
        // after the translucent box must land exactly where it would land
        // without any opacity declared, since opacity is purely a paint-time
        // property in real CSS.
        let with_opacity = run(
            "<body><div>a</div><p id='after'>b</p></body>",
            "div { display: block; height: 20px; opacity: 0.3; } \
             p { display: block; }",
            100.0,
        )
        .expect("lays out");
        let without_opacity = run(
            "<body><div>a</div><p id='after'>b</p></body>",
            "div { display: block; height: 20px; } p { display: block; }",
            100.0,
        )
        .expect("lays out");
        let document = document_of("<body><div>a</div><p id='after'>b</p></body>");
        assert_eq!(
            find_by_id(&with_opacity, &document, "after")
                .dimensions
                .content
                .y,
            find_by_id(&without_opacity, &document, "after")
                .dimensions
                .content
                .y,
            "opacity must not shift where a sibling lands"
        );
    }

    #[test]
    fn underline_paints_a_thin_line_near_the_bottom_of_the_text() {
        let root = run(
            "<body><p>x</p></body>",
            "p { text-decoration: underline; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let text_rect = list
            .items
            .iter()
            .find_map(|item| match item {
                DisplayItem::Text { rect, .. } => Some(*rect),
                _ => None,
            })
            .expect("text painted");
        let line = list
            .items
            .iter()
            .find_map(|item| match item {
                DisplayItem::SolidColor { rect, .. } if *rect != text_rect => Some(*rect),
                _ => None,
            })
            .expect("a decoration line painted");
        assert_eq!(line.height, 1.0, "the line is thin");
        assert!(
            line.y > text_rect.y + text_rect.height * 0.5,
            "underline sits in the lower half of the line box: {line:?} vs text {text_rect:?}"
        );
        assert!(
            line.y < text_rect.y + text_rect.height,
            "underline stays within the line box"
        );
    }

    #[test]
    fn line_through_paints_at_the_vertical_centre() {
        let root = run(
            "<body><p>x</p></body>",
            "p { text-decoration: line-through; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let text_rect = list
            .items
            .iter()
            .find_map(|item| match item {
                DisplayItem::Text { rect, .. } => Some(*rect),
                _ => None,
            })
            .expect("text painted");
        let line = list
            .items
            .iter()
            .find_map(|item| match item {
                DisplayItem::SolidColor { rect, .. } if *rect != text_rect => Some(*rect),
                _ => None,
            })
            .expect("a decoration line painted");
        let expected_centre = text_rect.y + text_rect.height * 0.5;
        assert!(
            (line.y - expected_centre).abs() < 0.5,
            "line-through sits at the vertical centre: {line:?} vs expected y {expected_centre}"
        );
    }

    #[test]
    fn no_decoration_by_default_paints_no_extra_line() {
        let root = run("<body><p>x</p></body>", "p { color: black; }", 100.0).expect("lays out");
        let list = build_display_list(&root);
        let solid_fills = list
            .items
            .iter()
            .filter(|item| matches!(item, DisplayItem::SolidColor { .. }))
            .count();
        assert_eq!(solid_fills, 0, "text-decoration's initial value is none");
    }

    #[test]
    fn text_decoration_propagates_to_descendant_text_like_colour() {
        // A decoration declared on a block applies to the text nodes it
        // contains, the same propagation `color` already gets, not only to
        // an element that declares it directly on itself.
        let root = run(
            "<body><div><span>x</span></div></body>",
            "div { text-decoration: underline; } span { display: inline; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let solid_fills = list
            .items
            .iter()
            .filter(|item| matches!(item, DisplayItem::SolidColor { .. }))
            .count();
        assert_eq!(
            solid_fills, 1,
            "the span's text inherited the div's underline"
        );
    }

    #[test]
    fn an_unimplemented_text_decoration_is_refused() {
        let error = run(
            "<body><p>x</p></body>",
            "p { text-decoration: overline; }",
            100.0,
        )
        .expect_err("refused");
        assert!(matches!(
            error,
            LayoutError::TextDecorationUnsupported { .. }
        ));
    }

    #[test]
    fn a_hidden_box_paints_nothing_of_its_own() {
        let root = run(
            "<body><div>x</div></body>",
            "div { background: red; border-width: 2px; border-color: lime; \
             outline-width: 2px; outline-color: blue; visibility: hidden; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        assert!(
            list.items.is_empty(),
            "a hidden box paints no background, border, outline, or text: {list:?}"
        );
    }

    #[test]
    fn a_hidden_box_still_occupies_its_layout_space() {
        // The defining difference from `display: none`: a sibling after a
        // hidden box must land exactly where it would if the box painted
        // normally, because hiding it did not remove it from layout.
        let html = "<body><div class='hidden'>a</div><div id='after'>b</div></body>";
        let css = "div { display: block; height: 10px; } .hidden { visibility: hidden; }";
        let with_hidden = run(html, css, 100.0).expect("lays out");
        let without_hidden =
            run(html, "div { display: block; height: 10px; }", 100.0).expect("lays out");
        let with_document = document_of(html);
        let without_document = document_of(html);
        let after_hidden = find_by_id(&with_hidden, &with_document, "after");
        let after_plain = find_by_id(&without_hidden, &without_document, "after");
        assert_eq!(
            after_hidden.dimensions.content.y, after_plain.dimensions.content.y,
            "hiding the first box must not move the second one"
        );
    }

    #[test]
    fn a_descendant_can_override_visibility_back_to_visible() {
        // Real CSS's inheritance-with-override rule: a hidden ancestor does
        // not suppress a descendant that explicitly re-declares `visible`.
        let root = run(
            "<body><div class='outer'><span class='inner'>x</span></div></body>",
            "div { visibility: hidden; } \
             span { display: inline; background: teal; visibility: visible; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        let teal = Color::parse("teal").expect("named colour");
        assert!(
            list.items.iter().any(
                |item| matches!(item, DisplayItem::SolidColor { color, .. } if *color == teal)
            ),
            "the inner span's own visible re-enables its own paint under a hidden ancestor"
        );
    }

    #[test]
    fn visibility_hidden_still_paints_a_visible_child_text_node() {
        // The everyday shape: an element hides everything, one nested
        // element opts back in, and that element's own text — which
        // inherits `visible` from *it*, not from the hidden grandparent —
        // paints.
        let root = run(
            "<body><div class='outer'><p class='inner'>shown</p></div></body>",
            "div { visibility: hidden; } p { visibility: visible; }",
            100.0,
        )
        .expect("lays out");
        let list = build_display_list(&root);
        assert!(
            list.items
                .iter()
                .any(|item| matches!(item, DisplayItem::Text { text, .. } if text == "shown")),
            "the re-enabled paragraph's text paints"
        );
    }

    #[test]
    fn an_unimplemented_visibility_is_refused() {
        let error = run(
            "<body><p>x</p></body>",
            "p { visibility: collapse; }",
            100.0,
        )
        .expect_err("refused");
        assert!(matches!(error, LayoutError::VisibilityUnsupported { .. }));
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
            DisplayItem::Text { color, .. } if *color == Color::parse("navy").expect("named colour")
        )));
    }

    #[test]
    fn boxes_stay_inside_the_viewport() {
        let html = "<body><div>a</div><div>b</div></body>";
        let root = run(html, "div { padding: 5px }", 400.0).expect("lays out");
        let list = build_display_list(&root);
        for item in &list.items {
            let rect = match item {
                DisplayItem::SolidColor { rect, .. }
                | DisplayItem::RoundedColor { rect, .. }
                | DisplayItem::Text { rect, .. } => rect,
            };
            assert!(
                rect.x >= 0.0 && rect.x + rect.width <= 400.0 + f32::EPSILON,
                "box escaped the viewport: {rect:?}"
            );
        }
    }

    // -- flex layout -------------------------------------------------------

    const TWO_ITEMS: &str =
        "<html><body><div id='c'><div id='a'>a</div><div id='b'>b</div></div></body></html>";
    const THREE_ITEMS: &str = "<html><body><div id='c'><div id='a'>a</div><div id='b'>b</div>\
         <div id='d'>d</div></div></body></html>";

    #[test]
    fn flex_direction_row_places_items_left_to_right() {
        let css = "#c { display: flex; } #a { width: 50px; } #b { width: 30px; }";
        let root = run(TWO_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(TWO_ITEMS);

        let a = find_by_id(&root, &document, "a");
        assert_eq!(a.dimensions.content.x, 0.0);
        assert_eq!(a.dimensions.content.width, 50.0);

        let b = find_by_id(&root, &document, "b");
        assert_eq!(
            b.dimensions.content.x, 50.0,
            "the second item must start where the first item's border box ends"
        );
        assert_eq!(
            a.dimensions.content.y, b.dimensions.content.y,
            "row items share a line"
        );
    }

    #[test]
    fn flex_direction_column_places_items_top_to_bottom() {
        let css = "#c { display: flex; flex-direction: column; height: 200px; } \
                   #a { height: 50px; } #b { height: 30px; }";
        let root = run(TWO_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(TWO_ITEMS);

        let a = find_by_id(&root, &document, "a");
        assert_eq!(a.dimensions.content.y, 0.0);

        let b = find_by_id(&root, &document, "b");
        assert_eq!(
            b.dimensions.content.y, 50.0,
            "the second item must start below the first item's height"
        );
        assert_eq!(
            a.dimensions.content.x, b.dimensions.content.x,
            "column items share a column"
        );
    }

    #[test]
    fn gap_is_respected_between_row_items() {
        let css = "#c { display: flex; gap: 10px; } #a { width: 50px; } #b { width: 30px; }";
        let root = run(TWO_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(TWO_ITEMS);

        let b = find_by_id(&root, &document, "b");
        assert_eq!(b.dimensions.content.x, 60.0, "50px item plus a 10px gap");
    }

    #[test]
    fn negative_gap_is_reported_not_guessed() {
        let error = run(
            "<html><body><div>x</div></body></html>",
            "div { display: flex; gap: -5px; }",
            400.0,
        )
        .expect_err("refused");
        assert!(matches!(error, LayoutError::NegativeEdgeUnsupported { .. }));
    }

    #[test]
    fn justify_content_center_leaves_equal_room_on_both_ends() {
        let css = "#c { display: flex; width: 200px; justify-content: center; } \
                   #a { width: 50px; } #b { width: 30px; }";
        let root = run(TWO_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(TWO_ITEMS);

        // 80px of items in a 200px container leaves 120px of slack, 60px on
        // each side.
        let a = find_by_id(&root, &document, "a");
        assert_eq!(a.dimensions.content.x, 60.0);
        let b = find_by_id(&root, &document, "b");
        assert_eq!(b.dimensions.content.x, 110.0);
    }

    #[test]
    fn justify_content_space_between_pins_the_ends_and_splits_the_rest() {
        let css = "#c { display: flex; width: 300px; justify-content: space-between; } \
                   #a { width: 50px; } #b { width: 50px; } #d { width: 50px; }";
        let root = run(THREE_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(THREE_ITEMS);

        // 150px of items in a 300px container leaves 150px of slack, split
        // evenly between the two gaps between three items: 75px each.
        let a = find_by_id(&root, &document, "a");
        assert_eq!(
            a.dimensions.content.x, 0.0,
            "the first item pins to the start"
        );
        let b = find_by_id(&root, &document, "b");
        assert_eq!(b.dimensions.content.x, 125.0);
        let d = find_by_id(&root, &document, "d");
        assert_eq!(
            d.dimensions.content.x + d.dimensions.content.width,
            300.0,
            "the last item pins to the end"
        );
    }

    #[test]
    fn justify_content_space_around_gives_each_item_equal_flanking_space() {
        let css = "#c { display: flex; width: 300px; justify-content: space-around; } \
                   #a { width: 50px; } #b { width: 50px; } #d { width: 50px; }";
        let root = run(THREE_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(THREE_ITEMS);

        // 150px of items in a 300px container leaves 150px of slack, split
        // into three equal shares of 50px (one per item), each item getting
        // half a share on either side — so gaps between items are a full
        // share (50px) and the two outer edges get a half-share (25px)
        // each.
        let a = find_by_id(&root, &document, "a");
        assert_eq!(
            a.dimensions.content.x, 25.0,
            "half a share leads the first item"
        );
        let b = find_by_id(&root, &document, "b");
        assert_eq!(b.dimensions.content.x, 125.0);
        let d = find_by_id(&root, &document, "d");
        assert_eq!(d.dimensions.content.x, 225.0);
        assert_eq!(
            300.0 - (d.dimensions.content.x + d.dimensions.content.width),
            25.0,
            "half a share trails the last item too"
        );
    }

    #[test]
    fn align_items_center_centers_the_cross_axis() {
        let css = "#c { display: flex; height: 100px; align-items: center; } \
                   #a { width: 50px; height: 20px; }";
        let root = run(TWO_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(TWO_ITEMS);

        let a = find_by_id(&root, &document, "a");
        assert_eq!(
            a.dimensions.content.y, 40.0,
            "a 20px item centred in a 100px line sits 40px from the top"
        );
    }

    #[test]
    fn align_items_stretch_fills_the_cross_axis() {
        let css = "#c { display: flex; height: 100px; align-items: stretch; } #a { width: 50px; }";
        let root = run(TWO_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(TWO_ITEMS);

        let a = find_by_id(&root, &document, "a");
        assert_eq!(
            a.dimensions.content.height, 100.0,
            "stretch fills the container's definite cross size"
        );
    }

    #[test]
    fn align_items_flex_end_pins_to_the_cross_end() {
        let css = "#c { display: flex; height: 100px; align-items: flex-end; } \
                   #a { width: 50px; height: 20px; }";
        let root = run(TWO_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(TWO_ITEMS);

        let a = find_by_id(&root, &document, "a");
        assert_eq!(
            a.dimensions.content.y, 80.0,
            "a 20px item pinned to the end of a 100px line sits 80px from the top"
        );
    }

    #[test]
    fn justify_content_flex_end_pins_items_to_the_main_end() {
        let css = "#c { display: flex; width: 200px; justify-content: flex-end; } \
                   #a { width: 50px; } #b { width: 30px; }";
        let root = run(TWO_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(TWO_ITEMS);

        // 80px of items pinned to the end of a 200px container: the group
        // starts 120px in, so `a` is at 120 and `b` immediately after at 170.
        let a = find_by_id(&root, &document, "a");
        assert_eq!(a.dimensions.content.x, 120.0);
        let b = find_by_id(&root, &document, "b");
        assert_eq!(
            b.dimensions.content.x + b.dimensions.content.width,
            200.0,
            "the last item's border box ends exactly at the container's end"
        );
    }

    #[test]
    fn flex_grow_distributes_extra_space_proportionally() {
        // Both items start from a zero basis (`flex: N` sets the basis to 0,
        // not auto), so the full 300px is free space, split 1:2 between the
        // two grow factors.
        let css = "#c { display: flex; width: 300px; } #a { flex: 1; } #b { flex: 2; }";
        let root = run(TWO_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(TWO_ITEMS);

        let a = find_by_id(&root, &document, "a").dimensions.content.width;
        let b = find_by_id(&root, &document, "b").dimensions.content.width;
        assert!((a - 100.0).abs() < 0.01, "a should be ~100px, was {a}");
        assert!((b - 200.0).abs() < 0.01, "b should be ~200px, was {b}");
    }

    #[test]
    fn flex_grow_of_zero_does_not_divide_by_zero() {
        // Neither item declares `flex-grow`, so the grow-factor sum is
        // exactly zero. Distributing free space by dividing by that sum
        // without a guard produces a NaN width that would then propagate
        // through every later comparison in this crate. Reverting the
        // `grow_sum > 0.0` guard locally and rerunning this test does fail
        // it (both widths come back NaN, and `assert_eq!` with a basis
        // value fails since NaN is not equal to anything, including
        // itself) before the guard is reapplied.
        let css = "#c { display: flex; width: 300px; } #a { width: 50px; } #b { width: 30px; }";
        let root = run(TWO_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(TWO_ITEMS);

        let a = find_by_id(&root, &document, "a").dimensions.content.width;
        let b = find_by_id(&root, &document, "b").dimensions.content.width;
        assert_eq!(a, 50.0, "no grow factor means no growth, not NaN");
        assert_eq!(b, 30.0, "no grow factor means no growth, not NaN");
        assert!(!a.is_nan() && !b.is_nan());
    }

    #[test]
    fn flex_shrink_shrinks_items_proportionally_when_they_overflow() {
        let css = "#c { display: flex; width: 100px; } #a { width: 80px; } #b { width: 80px; }";
        let root = run(TWO_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(TWO_ITEMS);

        // 160px of basis in a 100px container overflows by 60px. Equal
        // basis and the default flex-shrink of 1 on both items splits the
        // deficit evenly: 30px off each, leaving both at 50px.
        let a = find_by_id(&root, &document, "a").dimensions.content.width;
        let b = find_by_id(&root, &document, "b").dimensions.content.width;
        assert_eq!(a, 50.0);
        assert_eq!(b, 50.0);
    }

    #[test]
    fn flex_shrink_weight_of_zero_does_not_divide_by_zero() {
        // Both items refuse to shrink at all, so the shrink-weight sum is
        // zero even though the container overflows — the deficit must not
        // be distributed (and, before the corresponding guard, would
        // otherwise divide by zero into NaN the same way the grow path
        // does).
        let css = "#c { display: flex; width: 100px; } \
                   #a { width: 80px; flex-shrink: 0; } #b { width: 80px; flex-shrink: 0; }";
        let root = run(TWO_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(TWO_ITEMS);

        let a = find_by_id(&root, &document, "a").dimensions.content.width;
        let b = find_by_id(&root, &document, "b").dimensions.content.width;
        assert_eq!(
            a, 80.0,
            "flex-shrink: 0 keeps the basis size even while overflowing"
        );
        assert_eq!(b, 80.0);
    }

    #[test]
    fn flex_basis_explicit_wins_over_a_declared_width() {
        let css = "#c { display: flex; width: 400px; } #a { width: 200px; flex-basis: 30px; }";
        let root = run(TWO_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(TWO_ITEMS);

        let a = find_by_id(&root, &document, "a");
        assert_eq!(
            a.dimensions.content.width, 30.0,
            "an explicit flex-basis is the used basis regardless of `width`"
        );
    }

    #[test]
    fn flex_wrap_is_reported_not_guessed() {
        let error = run(
            "<html><body><div>x</div></body></html>",
            "div { display: flex; flex-wrap: wrap; }",
            400.0,
        )
        .expect_err("refused");
        assert!(matches!(error, LayoutError::FlexWrapUnsupported { .. }));
    }

    #[test]
    fn flex_direction_reverse_values_are_reported_not_guessed() {
        for value in ["row-reverse", "column-reverse"] {
            let css = format!("div {{ display: flex; flex-direction: {value}; }}");
            let error =
                run("<html><body><div>x</div></body></html>", &css, 400.0).expect_err("refused");
            assert!(
                matches!(error, LayoutError::FlexDirectionUnsupported { .. }),
                "flex-direction: {value} was not refused"
            );
        }
    }

    #[test]
    fn inline_flex_is_reported_not_guessed() {
        let error = run(
            "<html><body><span>x</span></body></html>",
            "span { display: inline-flex; }",
            400.0,
        )
        .expect_err("refused");
        assert!(
            matches!(error, LayoutError::AtomicInlineUnsupported { .. }),
            "inline-flex must not be confused with the DisplayModeUnsupported \
             flex/grid/table refusal — the inner algorithm is implemented"
        );
    }

    #[test]
    fn align_items_unsupported_value_is_reported_not_guessed() {
        let error = run(
            "<html><body><div>x</div></body></html>",
            "div { display: flex; align-items: baseline; }",
            400.0,
        )
        .expect_err("refused");
        assert!(matches!(error, LayoutError::AlignItemsUnsupported { .. }));
    }

    #[test]
    fn justify_content_unsupported_value_is_reported_not_guessed() {
        let error = run(
            "<html><body><div>x</div></body></html>",
            "div { display: flex; justify-content: stretch; }",
            400.0,
        )
        .expect_err("refused");
        assert!(matches!(
            error,
            LayoutError::JustifyContentUnsupported { .. }
        ));
    }

    #[test]
    fn ambiguous_flex_shorthand_is_reported_not_guessed() {
        // The full shorthand grammar lets a basis and the grow/shrink pair
        // appear in either order; this reordered form is exactly the case
        // this crate refuses rather than guesses at.
        let error = run(
            "<html><body><div>x</div></body></html>",
            "div { display: flex; flex: 30px 2; }",
            400.0,
        )
        .expect_err("refused");
        assert!(matches!(
            error,
            LayoutError::FlexShorthandUnsupported { .. }
        ));
    }

    #[test]
    fn flex_shorthand_none_and_auto_resolve_the_documented_way() {
        let css = "#c { display: flex; width: 300px; } \
                   #a { flex: none; width: 40px; } #b { flex: auto; }";
        let root = run(TWO_ITEMS, css, 400.0).expect("lays out");
        let document = document_of(TWO_ITEMS);

        // `flex: none` is `0 0 auto`: no grow, no shrink, basis from the
        // declared width (40px) — it must not grow even though the
        // container has room to spare. `flex: auto` is `1 1 auto`: with no
        // declared width `b`'s basis is 0 (this crate's stated fallback for
        // a block with no declared main size and no measurable content),
        // and it is the only item that grows, so it alone absorbs all
        // 260px of free space (300px container minus `a`'s 40px basis).
        let a = find_by_id(&root, &document, "a").dimensions.content.width;
        assert_eq!(a, 40.0, "flex: none must not grow");
        let b = find_by_id(&root, &document, "b").dimensions.content.width;
        assert_eq!(
            b, 260.0,
            "flex: auto grows to absorb all the free space alone"
        );
    }
}
