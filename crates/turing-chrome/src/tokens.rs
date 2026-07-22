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

pub use turing_runtime::{DARK, LIGHT, Theme};

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
