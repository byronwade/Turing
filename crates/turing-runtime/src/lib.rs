// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Turing's retained component runtime for application UI.
//!
//! This is the first executable slice of the platform architecture described
//! in `docs/application-runtime/01-turing-platform-architecture.md`. It is a
//! native representation of JSX-shaped component output: components are
//! constructed as a typed tree, the tree is flattened into the shared Turing
//! paint vocabulary, and hit regions are emitted from the same geometry.
//!
//! The runtime deliberately owns no browser policy, page DOM, credentials,
//! navigation, or platform window handles. An application supplies state and
//! maps the returned hit identifiers to typed commands. That keeps the
//! component runtime reusable by the browser, future Nova applications, and
//! headless fixture tests without making it a second browser engine.

#![forbid(unsafe_code)]

use turing_css::Color;
use turing_layout::{Point, Rect};
use turing_paint::{PaintItem, PaintList};

/// Stable semantic component kinds used in frame traces and fixture reports.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ComponentKind {
    /// Root application composition.
    Application,
    /// Window-level trusted chrome.
    WindowChrome,
    /// Top navigation and tab strip.
    Toolbar,
    /// One tab in a tab strip.
    Tab,
    /// Address/search field.
    AddressField,
    /// Navigation or command button.
    Button,
    /// Left or right application rail.
    Sidebar,
    /// Main route content.
    Viewport,
    /// Repeated content card.
    Card,
    /// Repeated list row.
    ListRow,
    /// Modal or command surface.
    Dialog,
    /// Bottom status surface.
    StatusBar,
    /// Text node produced by a component.
    Text,
}

/// A design-system palette shared by every runtime surface.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct Theme {
    /// Window background.
    pub ink: Color,
    /// Base panel surface.
    pub surface1: Color,
    /// Toolbar and elevated surface.
    pub surface2: Color,
    /// Hover and active surface.
    pub surface3: Color,
    /// Pressed surface.
    pub surface4: Color,
    /// Hairline border.
    pub line: Color,
    /// Strong border and focus ring.
    pub line2: Color,
    /// Primary text.
    pub text: Color,
    /// Secondary text.
    pub text2: Color,
    /// Tertiary text and placeholders.
    pub text3: Color,
    /// Accent role.
    pub accent: Color,
    /// Accent background role.
    pub accent_soft: Color,
    /// Success role.
    pub good: Color,
    /// Warning role.
    pub warn: Color,
    /// Error role.
    pub bad: Color,
}

const fn rgb(hex: u32) -> Color {
    Color {
        red: ((hex >> 16) & 0xFF) as u8,
        green: ((hex >> 8) & 0xFF) as u8,
        blue: (hex & 0xFF) as u8,
    }
}

const GLYPH_ADVANCE: f32 = 8.0;

/// Nova dark theme.
pub const DARK: Theme = Theme {
    ink: rgb(0x0A0A0A),
    surface1: rgb(0x101012),
    surface2: rgb(0x141416),
    surface3: rgb(0x1B1B1E),
    surface4: rgb(0x212125),
    line: rgb(0x262628),
    line2: rgb(0x333335),
    text: rgb(0xEDEDED),
    text2: rgb(0x9A9A9F),
    text3: rgb(0x616166),
    accent: rgb(0x2E8DFF),
    accent_soft: rgb(0x171F36),
    good: rgb(0x34D399),
    warn: rgb(0xFBBF24),
    bad: rgb(0xF87171),
};

/// Nova light theme.
pub const LIGHT: Theme = Theme {
    ink: rgb(0xFBFBFC),
    surface1: rgb(0xFFFFFF),
    surface2: rgb(0xF7F8F9),
    surface3: rgb(0xEEF0F2),
    surface4: rgb(0xE2E5E8),
    line: rgb(0xE9EBEE),
    line2: rgb(0xD9DDE2),
    text: rgb(0x17181A),
    text2: rgb(0x4B5057),
    text3: rgb(0x8F959D),
    accent: rgb(0x2E8DFF),
    accent_soft: rgb(0xE1ECFB),
    good: rgb(0x0F9955),
    warn: rgb(0xC07C1D),
    bad: rgb(0xDC3535),
};

/// Comfortable Nova density values.
pub mod spacing {
    /// Top toolbar height.
    pub const TOOLBAR: f32 = 52.0;
    /// Bottom status height.
    pub const STATUS: f32 = 42.0;
    /// Standard page inset.
    pub const PAGE: f32 = 28.0;
    /// Sidebar width.
    pub const SIDEBAR: f32 = 224.0;
    /// Compact sidebar width.
    pub const SIDEBAR_COMPACT: f32 = 64.0;
    /// Standard component gap.
    pub const GAP: f32 = 10.0;
    /// Large component gap.
    pub const GUTTER: f32 = 20.0;
    /// Standard radius.
    pub const RADIUS_SM: f32 = 7.0;
    /// Standard Nova radius.
    pub const RADIUS: f32 = 10.0;
    /// Large radius.
    pub const RADIUS_LG: f32 = 14.0;
}

/// Motion tokens are kept in the runtime even though the first raster
/// presenter redraws on state changes instead of running a compositor clock.
pub mod motion {
    /// Fast hover transition.
    pub const FAST_MS: u16 = 80;
    /// Standard surface transition.
    pub const STANDARD_MS: u16 = 120;
    /// Route transition.
    pub const ROUTE_MS: u16 = 180;
}

/// A hit identifier is interpreted by the owning application, never by the
/// runtime. The high byte is reserved for component family; the remaining
/// bits are application-owned stable identity.
pub type HitId = u64;

/// One declarative component node. This is the native runtime's JSX-shaped
/// intermediate representation for the first prototype.
#[derive(Clone, Debug, PartialEq)]
pub struct Node {
    /// Semantic component kind.
    pub kind: ComponentKind,
    /// Bounds in window coordinates.
    pub rect: Rect,
    /// Optional fill.
    pub fill: Option<Color>,
    /// Optional border.
    pub border: Option<Color>,
    /// Corner radius for fill and border.
    pub radius: f32,
    /// Optional single-line text content.
    pub text: Option<String>,
    /// Text color when `text` exists.
    pub text_color: Color,
    /// Optional hit target.
    pub hit: Option<HitId>,
    /// Child components in paint order.
    pub children: Vec<Self>,
}

impl Node {
    /// Creates an empty component node.
    #[must_use]
    pub fn new(kind: ComponentKind, rect: Rect) -> Self {
        Self {
            kind,
            rect,
            fill: None,
            border: None,
            radius: 0.0,
            text: None,
            text_color: LIGHT.text,
            hit: None,
            children: Vec::new(),
        }
    }

    /// Sets the fill role.
    #[must_use]
    pub const fn fill(mut self, color: Color) -> Self {
        self.fill = Some(color);
        self
    }

    /// Sets border and corner radius.
    #[must_use]
    pub const fn border(mut self, color: Color, radius: f32) -> Self {
        self.border = Some(color);
        self.radius = radius;
        self
    }

    /// Sets text content and color.
    #[must_use]
    pub fn text(mut self, value: impl Into<String>, color: Color) -> Self {
        self.text = Some(value.into());
        self.text_color = color;
        self
    }

    /// Makes this component interactive.
    #[must_use]
    pub const fn hit(mut self, id: HitId) -> Self {
        self.hit = Some(id);
        self
    }

    /// Appends one child component.
    #[must_use]
    pub fn child(mut self, child: Self) -> Self {
        self.children.push(child);
        self
    }

    /// Appends multiple child components.
    #[must_use]
    pub fn children(mut self, children: impl IntoIterator<Item = Self>) -> Self {
        self.children.extend(children);
        self
    }
}

/// One component in the inspectable frame tree.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct ComponentRecord {
    /// Semantic kind.
    pub kind: ComponentKind,
    /// Bounds.
    pub rect: Rect,
    /// Application-owned interaction target.
    pub hit: Option<HitId>,
}

/// A rendered frame and its inspectable interaction geometry.
#[derive(Clone, Debug, Default, PartialEq)]
pub struct Frame {
    /// Shared paint representation.
    pub paint: PaintList,
    /// Hit regions in front-to-back traversal order.
    pub hits: Vec<ComponentRecord>,
    /// Component records for runtime inspection and fixture tests.
    pub components: Vec<ComponentRecord>,
}

impl Frame {
    /// Returns the top-most hit target at a point.
    #[must_use]
    pub fn hit_test(&self, point: Point) -> Option<HitId> {
        self.hits
            .iter()
            .rev()
            .find(|record| record.hit.is_some_and(|_| contains(record.rect, point)))
            .and_then(|record| record.hit)
    }

    /// Counts nodes of one semantic kind.
    #[must_use]
    pub fn count(&self, kind: ComponentKind) -> usize {
        self.components
            .iter()
            .filter(|record| record.kind == kind)
            .count()
    }
}

/// Retained component runtime. The runtime is stateless; the owner supplies a
/// new tree from its immutable snapshot on every invalidated frame.
#[derive(Clone, Copy, Debug, Default)]
pub struct Runtime;

impl Runtime {
    /// Flattens a component tree into paint and inspectable hit regions.
    #[must_use]
    pub fn render(root: &Node) -> Frame {
        let mut frame = Frame::default();
        paint_node(root, &mut frame);
        frame
    }
}

fn contains(rect: Rect, point: Point) -> bool {
    point.x >= rect.x
        && point.x < rect.x + rect.width
        && point.y >= rect.y
        && point.y < rect.y + rect.height
}

fn inset(rect: Rect, amount: f32) -> Rect {
    Rect {
        x: rect.x + amount,
        y: rect.y + amount,
        width: (rect.width - amount * 2.0).max(0.0),
        height: (rect.height - amount * 2.0).max(0.0),
    }
}

fn paint_node(node: &Node, frame: &mut Frame) {
    let record = ComponentRecord {
        kind: node.kind,
        rect: node.rect,
        hit: node.hit,
    };
    frame.components.push(record);
    if node.hit.is_some() {
        frame.hits.push(record);
    }

    if let Some(border) = node.border {
        frame.paint.items.push(PaintItem::Fill {
            rect: node.rect,
            color: border,
            alpha: 1.0,
            radius: node.radius,
        });
    }
    if let Some(fill) = node.fill {
        frame.paint.items.push(PaintItem::Fill {
            rect: if node.border.is_some() {
                inset(node.rect, 1.0)
            } else {
                node.rect
            },
            color: fill,
            alpha: 1.0,
            radius: (node.radius - 1.0).max(0.0),
        });
    }
    if let Some(text) = &node.text {
        #[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
        let capacity = (node.rect.width / GLYPH_ADVANCE).floor().max(0.0) as usize;
        let shown: String = text.chars().take(capacity).collect();
        #[allow(clippy::cast_precision_loss)]
        let text_width = shown.chars().count() as f32 * GLYPH_ADVANCE;
        frame.paint.items.push(PaintItem::Text {
            rect: Rect {
                x: node.rect.x,
                y: node.rect.y,
                width: text_width,
                height: node.rect.height,
            },
            text: shown,
            color: node.text_color,
            alpha: 1.0,
        });
    }
    for child in &node.children {
        paint_node(child, frame);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn rect(x: f32, y: f32, width: f32, height: f32) -> Rect {
        Rect {
            x,
            y,
            width,
            height,
        }
    }

    #[test]
    fn runtime_paints_and_indexes_the_same_component_tree() {
        let tree = Node::new(ComponentKind::Application, rect(0.0, 0.0, 100.0, 60.0)).child(
            Node::new(ComponentKind::Button, rect(10.0, 10.0, 50.0, 24.0))
                .fill(LIGHT.surface3)
                .text("Open", LIGHT.text)
                .hit(7),
        );
        let frame = Runtime::render(&tree);
        assert_eq!(frame.count(ComponentKind::Button), 1);
        assert_eq!(frame.hit_test(Point { x: 20.0, y: 20.0 }), Some(7));
        assert!(frame.paint.items.len() >= 2);
    }

    #[test]
    fn hit_testing_prefers_the_frontmost_component() {
        let tree = Node::new(ComponentKind::Application, rect(0.0, 0.0, 100.0, 60.0))
            .child(Node::new(ComponentKind::Button, rect(10.0, 10.0, 50.0, 24.0)).hit(1))
            .child(Node::new(ComponentKind::Button, rect(20.0, 15.0, 50.0, 24.0)).hit(2));
        assert_eq!(
            Runtime::render(&tree).hit_test(Point { x: 25.0, y: 20.0 }),
            Some(2)
        );
    }
}
