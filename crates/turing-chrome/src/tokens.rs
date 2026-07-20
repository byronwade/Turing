// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Nova design tokens, mirrored from `design/tokens.json`.
//!
//! The JSON file is the shared source of truth prescribed by
//! `docs/ui-runtime/06-react-design-lab-tokens-and-authoring-workflow.md`;
//! these constants are its Rust projection, and a value changed here without
//! changing there is a defect. Alpha-composited source tokens carry their
//! flattened opaque equivalents, because the reference rasterizer paints
//! opaque colours only; the flattening surface is recorded in the JSON.

use turing_css::Color;

const fn rgb(hex: u32) -> Color {
    Color {
        red: ((hex >> 16) & 0xFF) as u8,
        green: ((hex >> 8) & 0xFF) as u8,
        blue: (hex & 0xFF) as u8,
    }
}

/// One Nova theme, reduced to what the reference painter can use.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Theme {
    /// App base background behind page surfaces (`--ink`).
    pub ink: Color,
    /// Lowest surface (`--c1`): panels, the command palette.
    pub surface1: Color,
    /// Bar surface (`--c2`).
    pub surface2: Color,
    /// Hover / active-tab surface (`--c3`).
    pub surface3: Color,
    /// Pressed surface (`--c4`).
    pub surface4: Color,
    /// Hairline border (`--line`), flattened over surface 2.
    pub line: Color,
    /// Stronger border (`--line2`), flattened over surface 2.
    pub line2: Color,
    /// Primary text (`--tx`).
    pub text: Color,
    /// Secondary text (`--tx2`).
    pub text2: Color,
    /// Tertiary text and placeholders (`--tx3`).
    pub text3: Color,
    /// Accent (`--ac`).
    pub accent: Color,
    /// Accent fill (`--ac-soft`), flattened over surface 2.
    pub accent_soft: Color,
    /// Success (`--good`).
    pub good: Color,
}

/// Nova's dark theme (`:root`).
pub const DARK: Theme = Theme {
    ink: rgb(0x0a0a0a),
    surface1: rgb(0x101012),
    surface2: rgb(0x141416),
    surface3: rgb(0x1b1b1e),
    surface4: rgb(0x212125),
    line: rgb(0x262628),
    line2: rgb(0x333335),
    text: rgb(0xededed),
    text2: rgb(0x9a9a9f),
    text3: rgb(0x616166),
    accent: rgb(0x2e8dff),
    accent_soft: rgb(0x171f36),
    good: rgb(0x34d399),
};

/// Nova's light theme (`.nova.light`), the design's default app state.
pub const LIGHT: Theme = Theme {
    ink: rgb(0xfbfbfc),
    surface1: rgb(0xffffff),
    surface2: rgb(0xf7f8f9),
    surface3: rgb(0xeef0f2),
    surface4: rgb(0xe2e5e8),
    line: rgb(0xe9ebee),
    line2: rgb(0xd9dde2),
    text: rgb(0x17181a),
    text2: rgb(0x4b5057),
    text3: rgb(0x8f959d),
    accent: rgb(0x2e8dff),
    accent_soft: rgb(0xe1ecfb),
    good: rgb(0x0f9955),
};

/// `.bar` height, cozy density.
pub const BAR_HEIGHT: f32 = 44.0;
/// `.bar` horizontal padding.
pub const BAR_PADDING_X: f32 = 12.0;
/// Gap between bar clusters.
pub const BAR_GAP: f32 = 10.0;
/// `.ttab` height, cozy density.
pub const TAB_HEIGHT: f32 = 24.0;
/// `.ttab` horizontal padding.
pub const TAB_PADDING_X: f32 = 10.0;
/// Gap between tabs.
pub const TAB_GAP: f32 = 2.0;
/// `.ttab` width bounds and flex basis.
pub const TAB_MIN_WIDTH: f32 = 54.0;
pub const TAB_MAX_WIDTH: f32 = 190.0;
pub const TAB_FLEX_BASIS: f32 = 118.0;
/// `.xc` close button.
pub const CLOSE_SIZE: f32 = 16.0;
pub const CLOSE_RIGHT: f32 = 5.0;
/// `.newtab` button.
pub const NEW_TAB_SIZE: f32 = 28.0;
/// `.ib` icon button, cozy density.
pub const ICON_BUTTON_SIZE: f32 = 32.0;
/// `.site` pill.
pub const SITE_PILL_HEIGHT: f32 = 30.0;
pub const SITE_PILL_MAX_WIDTH: f32 = 420.0;
/// `.avatar`.
pub const AVATAR_SIZE: f32 = 24.0;

/// The command field's placeholder when a tab has no address yet
/// (`Search or enter address`).
pub const ADDRESS_PLACEHOLDER: &str = "Search or enter address";
/// The command palette input placeholder.
pub const PALETTE_PLACEHOLDER: &str = "Search the web or ask anything";
