// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Toolkit-neutral Nova chrome: shell state in, display list and typed
//! commands out.
//!
//! This crate renders the browser chrome described by the Nova design source
//! (`docs/ui-runtime/design-lab/turing-nova-design-source.jsx`) using the
//! engine's own display-list and raster contracts — the same pipeline that
//! paints pages paints the chrome. It consumes an immutable
//! [`turing_ui_model::ShellSnapshot`] and returns
//! [`turing_ui_model::ShellCommand`]s from pointer input; it never touches a
//! page, a renderer, or a privileged service, which is exactly the
//! state/command/adapter boundary the UI-runtime architecture prescribes.
//!
//! # Fidelity boundary
//!
//! The reference rasterizer paints opaque solid rectangles and 8x8 glyphs.
//! Nova's radii, shadows, blur, alpha, and motion are therefore recorded in
//! `design/tokens.json` but rendered flat, square, and static here. Layout
//! metrics, surface roles, and colour roles are token-exact; this is the
//! design's composition at reference fidelity, not its final finish.
//!
//! # Geometry is computed once
//!
//! Painting and hit testing share [`Geometry`]. A hit region that drifted
//! from its painted rectangle would be the chrome equivalent of routing
//! against stale layout, so it is made impossible the same way: one function
//! computes where things are, and both consumers read it.

#![forbid(unsafe_code)]

pub mod tokens;

use turing_css::Color;
use turing_layout::{DisplayItem, DisplayList, Point, Rect};
use turing_types::TabId;
use turing_ui_model::{ShellCommand, ShellSnapshot, TabLifecycle};

pub use tokens::{DARK, LIGHT, Theme};

/// Everything the chrome needs to draw one frame.
#[derive(Clone, Copy, Debug)]
pub struct ChromeModel<'a> {
    pub snapshot: &'a ShellSnapshot,
    /// Window width in CSS pixels.
    pub width: f32,
}

/// The chrome bar's height in CSS pixels (cozy density).
#[must_use]
pub const fn bar_height() -> f32 {
    tokens::BAR_HEIGHT
}

/// Where one tab is, for painting and hit testing.
#[derive(Clone, Copy, Debug)]
struct TabGeometry {
    tab: TabId,
    rect: Rect,
    close: Rect,
    active: bool,
    lifecycle: TabLifecycle,
}

/// Where everything in the bar is.
#[derive(Clone, Debug)]
struct Geometry {
    back: Rect,
    forward: Rect,
    reload: Rect,
    /// Tab chips, empty when the single-tab site pill is shown instead.
    tabs: Vec<TabGeometry>,
    /// The `.site` address pill, shown when exactly one tab exists.
    site_pill: Option<Rect>,
    new_tab: Rect,
    avatar: Rect,
}

const GLYPH_ADVANCE: f32 = 8.0;
const TEXT_LINE: f32 = 16.0;

fn icon_rect(x: f32) -> Rect {
    Rect {
        x,
        y: (tokens::BAR_HEIGHT - tokens::ICON_BUTTON_SIZE) / 2.0,
        width: tokens::ICON_BUTTON_SIZE,
        height: tokens::ICON_BUTTON_SIZE,
    }
}

fn contains(rect: Rect, point: Point) -> bool {
    point.x >= rect.x
        && point.x < rect.x + rect.width
        && point.y >= rect.y
        && point.y < rect.y + rect.height
}

fn geometry(model: &ChromeModel<'_>) -> Geometry {
    let back = icon_rect(tokens::BAR_PADDING_X);
    let forward = icon_rect(back.x + tokens::ICON_BUTTON_SIZE + 1.0);
    let reload = icon_rect(forward.x + tokens::ICON_BUTTON_SIZE + 1.0);

    let avatar = Rect {
        x: model.width - tokens::BAR_PADDING_X - tokens::AVATAR_SIZE,
        y: (tokens::BAR_HEIGHT - tokens::AVATAR_SIZE) / 2.0,
        width: tokens::AVATAR_SIZE,
        height: tokens::AVATAR_SIZE,
    };

    let strip_start = reload.x + tokens::ICON_BUTTON_SIZE + tokens::BAR_GAP;
    let strip_end = avatar.x - tokens::BAR_GAP;

    let tab_count = model.snapshot.tabs.len();
    let mut tabs = Vec::new();
    let mut site_pill = None;

    let new_tab_y = (tokens::BAR_HEIGHT - tokens::NEW_TAB_SIZE) / 2.0;
    let new_tab;

    if tab_count == 1 {
        // Nova shows the centred `.site` address pill for a single tab; the
        // pill doubles as the command-field opener.
        let span = (strip_end - strip_start - tokens::NEW_TAB_SIZE - tokens::BAR_GAP)
            .max(tokens::TAB_MIN_WIDTH);
        let width = span.min(tokens::SITE_PILL_MAX_WIDTH);
        let x = strip_start + (span - width) / 2.0;
        site_pill = Some(Rect {
            x,
            y: (tokens::BAR_HEIGHT - tokens::SITE_PILL_HEIGHT) / 2.0,
            width,
            height: tokens::SITE_PILL_HEIGHT,
        });
        new_tab = Rect {
            x: strip_end - tokens::NEW_TAB_SIZE,
            y: new_tab_y,
            width: tokens::NEW_TAB_SIZE,
            height: tokens::NEW_TAB_SIZE,
        };
    } else {
        #[allow(clippy::cast_precision_loss)]
        let count = tab_count.max(1) as f32;
        let available =
            strip_end - strip_start - tokens::NEW_TAB_SIZE - tokens::BAR_GAP - tokens::TAB_GAP;
        let width = (available / count - tokens::TAB_GAP)
            .clamp(tokens::TAB_MIN_WIDTH, tokens::TAB_MAX_WIDTH);
        let mut x = strip_start;
        let y = (tokens::BAR_HEIGHT - tokens::TAB_HEIGHT) / 2.0;
        for summary in &model.snapshot.tabs {
            let rect = Rect {
                x,
                y,
                width,
                height: tokens::TAB_HEIGHT,
            };
            let close = Rect {
                x: rect.x + rect.width - tokens::CLOSE_RIGHT - tokens::CLOSE_SIZE,
                y: rect.y + (rect.height - tokens::CLOSE_SIZE) / 2.0,
                width: tokens::CLOSE_SIZE,
                height: tokens::CLOSE_SIZE,
            };
            tabs.push(TabGeometry {
                tab: summary.id,
                rect,
                close,
                active: model.snapshot.active_tab == Some(summary.id),
                lifecycle: summary.lifecycle,
            });
            x += width + tokens::TAB_GAP;
        }
        new_tab = Rect {
            x: x + tokens::TAB_GAP,
            y: new_tab_y,
            width: tokens::NEW_TAB_SIZE,
            height: tokens::NEW_TAB_SIZE,
        };
    }

    Geometry {
        back,
        forward,
        reload,
        tabs,
        site_pill,
        new_tab,
        avatar,
    }
}

fn fill(list: &mut DisplayList, rect: Rect, color: Color) {
    list.items.push(DisplayItem::SolidColor { rect, color });
}

/// A one-pixel inset border drawn as four fills.
fn border(list: &mut DisplayList, rect: Rect, color: Color) {
    let Rect {
        x,
        y,
        width,
        height,
    } = rect;
    fill(
        list,
        Rect {
            x,
            y,
            width,
            height: 1.0,
        },
        color,
    );
    fill(
        list,
        Rect {
            x,
            y: y + height - 1.0,
            width,
            height: 1.0,
        },
        color,
    );
    fill(
        list,
        Rect {
            x,
            y,
            width: 1.0,
            height,
        },
        color,
    );
    fill(
        list,
        Rect {
            x: x + width - 1.0,
            y,
            width: 1.0,
            height,
        },
        color,
    );
}

/// Text centred vertically in `rect`, truncated with `..` when it cannot fit.
fn text_in(list: &mut DisplayList, rect: Rect, text: &str, color: Color, pad: f32) {
    #[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
    let capacity = (((rect.width - 2.0 * pad) / GLYPH_ADVANCE).floor().max(0.0)) as usize;
    if capacity == 0 {
        return;
    }
    let count = text.chars().count();
    let shown: String = if count <= capacity {
        text.to_owned()
    } else {
        let mut kept: String = text.chars().take(capacity.saturating_sub(2)).collect();
        kept.push_str("..");
        kept
    };
    #[allow(clippy::cast_precision_loss)]
    let width = shown.chars().count() as f32 * GLYPH_ADVANCE;
    list.items.push(DisplayItem::Text {
        rect: Rect {
            x: rect.x + pad,
            y: rect.y + (rect.height - TEXT_LINE) / 2.0,
            width,
            height: TEXT_LINE,
        },
        text: shown,
        color,
    });
}

/// A single glyph centred in `rect` — the reference stand-in for an icon.
fn glyph_in(list: &mut DisplayList, rect: Rect, glyph: char, color: Color) {
    list.items.push(DisplayItem::Text {
        rect: Rect {
            x: rect.x + (rect.width - GLYPH_ADVANCE) / 2.0,
            y: rect.y + (rect.height - TEXT_LINE) / 2.0,
            width: GLYPH_ADVANCE,
            height: TEXT_LINE,
        },
        text: glyph.to_string(),
        color,
    });
}

/// Paints the chrome bar for `model`.
///
/// Coordinates are window coordinates: the bar occupies
/// `y in [0, bar_height())` across the window's width.
#[must_use]
pub fn render(model: &ChromeModel<'_>, theme: &Theme) -> DisplayList {
    let geometry = geometry(model);
    let mut list = DisplayList::default();

    // The bar surface and its hairline bottom border.
    fill(
        &mut list,
        Rect {
            x: 0.0,
            y: 0.0,
            width: model.width,
            height: tokens::BAR_HEIGHT,
        },
        theme.surface2,
    );
    fill(
        &mut list,
        Rect {
            x: 0.0,
            y: tokens::BAR_HEIGHT - 1.0,
            width: model.width,
            height: 1.0,
        },
        theme.line,
    );

    // Navigation cluster. History does not exist yet, so back and forward
    // paint in the disabled `.ib.off` role rather than pretending.
    glyph_in(&mut list, geometry.back, '<', theme.text3);
    glyph_in(&mut list, geometry.forward, '>', theme.text3);
    glyph_in(&mut list, geometry.reload, 'R', theme.text2);

    if let Some(pill) = geometry.site_pill {
        fill(&mut list, pill, theme.surface3);
        let address = model
            .snapshot
            .tabs
            .first()
            .map(|tab| tab.display_url.as_str())
            .filter(|url| !url.is_empty() && *url != "about:blank");
        match address {
            Some(url) => {
                // The lock glyph paints in the success role for local
                // content the way Nova marks a secure origin.
                glyph_in(
                    &mut list,
                    Rect {
                        x: pill.x,
                        y: pill.y,
                        width: 24.0,
                        height: pill.height,
                    },
                    '*',
                    theme.good,
                );
                text_in(
                    &mut list,
                    Rect {
                        x: pill.x + 20.0,
                        y: pill.y,
                        width: pill.width - 24.0,
                        height: pill.height,
                    },
                    url,
                    theme.text2,
                    4.0,
                );
            }
            None => text_in(
                &mut list,
                pill,
                tokens::ADDRESS_PLACEHOLDER,
                theme.text3,
                14.0,
            ),
        }
    }

    for tab in &geometry.tabs {
        if tab.active {
            // `.ttab.on`: surface 3 with a 1px `--line2` inset ring.
            fill(&mut list, tab.rect, theme.line2);
            fill(
                &mut list,
                Rect {
                    x: tab.rect.x + 1.0,
                    y: tab.rect.y + 1.0,
                    width: tab.rect.width - 2.0,
                    height: tab.rect.height - 2.0,
                },
                theme.surface3,
            );
        }
        let title_color = match (tab.active, tab.lifecycle) {
            (true, _) => theme.text,
            // Stale tabs fade (`.ttab.s1/.s2`); opacity is approximated by
            // dropping to the tertiary text role.
            (false, TabLifecycle::Frozen | TabLifecycle::Discarded) => theme.text3,
            (false, _) => theme.text2,
        };
        let summary = model
            .snapshot
            .tabs
            .iter()
            .find(|candidate| candidate.id == tab.tab);
        let title = summary.map_or("", |summary| summary.title.as_str());
        let title = if title.is_empty() { "New Tab" } else { title };
        let title_rect = Rect {
            x: tab.rect.x,
            y: tab.rect.y,
            width: tab.rect.width - tokens::CLOSE_SIZE - tokens::CLOSE_RIGHT,
            height: tab.rect.height,
        };
        text_in(
            &mut list,
            title_rect,
            title,
            title_color,
            tokens::TAB_PADDING_X,
        );
        // Nova reveals the close affordance on hover; a static frame shows it
        // on the active tab, where the design also keeps it visible.
        if tab.active {
            glyph_in(&mut list, tab.close, 'x', theme.text3);
        }
    }

    glyph_in(&mut list, geometry.new_tab, '+', theme.text3);

    // Separator and avatar.
    fill(
        &mut list,
        Rect {
            x: geometry.avatar.x - tokens::BAR_GAP,
            y: (tokens::BAR_HEIGHT - 16.0) / 2.0,
            width: 1.0,
            height: 16.0,
        },
        theme.line2,
    );
    fill(&mut list, geometry.avatar, theme.surface3);
    border(&mut list, geometry.avatar, theme.line2);
    glyph_in(&mut list, geometry.avatar, 'T', theme.text2);

    list
}

/// Resolves a pointer press in window coordinates to a typed command.
///
/// Returns `None` for presses on inert chrome (the bar itself, disabled
/// navigation, the avatar) and for points outside the bar.
#[must_use]
pub fn command_at(model: &ChromeModel<'_>, point: Point) -> Option<ShellCommand> {
    if point.y >= tokens::BAR_HEIGHT {
        return None;
    }
    let geometry = geometry(model);

    if contains(geometry.new_tab, point) {
        return Some(ShellCommand::NewTab);
    }
    if contains(geometry.reload, point) {
        let tab = model.snapshot.active_tab?;
        return Some(ShellCommand::Reload { tab });
    }
    if let Some(pill) = geometry.site_pill
        && contains(pill, point)
    {
        return Some(ShellCommand::OpenCommandField {
            tab: model.snapshot.active_tab,
        });
    }
    for tab in &geometry.tabs {
        // The close region wins over the tab it sits inside.
        if tab.active && contains(tab.close, point) {
            return Some(ShellCommand::CloseTab { tab: tab.tab });
        }
        if contains(tab.rect, point) {
            // Nova: the active tab doubles as the address field, so
            // pressing it opens the command field rather than re-activating.
            return Some(if tab.active {
                ShellCommand::OpenCommandField { tab: Some(tab.tab) }
            } else {
                ShellCommand::ActivateTab { tab: tab.tab }
            });
        }
    }
    None
}

/// Paints the command palette over a `width` by `height` window.
///
/// `input` is the text typed so far; the palette shows the Nova placeholder
/// until the first character arrives. The veil's blur is not reproducible, so
/// the panel simply paints opaque on surface 1 with a `--line2` border.
#[must_use]
pub fn render_palette(width: f32, height: f32, input: &str, theme: &Theme) -> DisplayList {
    let mut list = DisplayList::default();
    let panel_width = (width * 0.94).min(900.0);
    let panel_height = (height * 0.74).min(590.0);
    let panel = Rect {
        x: (width - panel_width) / 2.0,
        y: (height - panel_height) * 0.25,
        width: panel_width,
        height: panel_height,
    };
    fill(&mut list, panel, theme.surface1);
    border(&mut list, panel, theme.line2);

    let input_row = Rect {
        x: panel.x + 1.0,
        y: panel.y + 1.0,
        width: panel.width - 2.0,
        height: 56.0,
    };
    if input.is_empty() {
        text_in(
            &mut list,
            input_row,
            tokens::PALETTE_PLACEHOLDER,
            theme.text3,
            18.0,
        );
    } else {
        let mut shown = input.to_owned();
        shown.push('_');
        text_in(&mut list, input_row, &shown, theme.text, 18.0);
    }
    fill(
        &mut list,
        Rect {
            x: panel.x + 1.0,
            y: input_row.y + input_row.height,
            width: panel.width - 2.0,
            height: 1.0,
        },
        theme.line,
    );
    text_in(
        &mut list,
        Rect {
            x: panel.x + 1.0,
            y: input_row.y + input_row.height + 8.0,
            width: panel.width - 2.0,
            height: 24.0,
        },
        "Enter opens a file path or address - Esc closes",
        theme.text3,
        18.0,
    );
    list
}

#[cfg(test)]
mod tests {
    use super::*;
    use turing_types::{ProfileId, SpaceId, TabId, ViewId, WindowId};
    use turing_ui_model::TabSummary;

    fn snapshot(count: u64, active: u64) -> ShellSnapshot {
        let tabs = (1..=count)
            .map(|index| TabSummary {
                id: TabId::new(index).expect("nonzero"),
                view: ViewId::new(index).expect("nonzero"),
                title: format!("Tab {index}"),
                display_url: format!("file:///{index}.html"),
                lifecycle: TabLifecycle::Active,
                protects_unsaved_work: false,
            })
            .collect();
        let snapshot = ShellSnapshot {
            version: 1,
            window: WindowId::new(1).expect("nonzero"),
            profile: ProfileId::new(1).expect("nonzero"),
            space: SpaceId::new(1).expect("nonzero"),
            active_tab: Some(TabId::new(active).expect("nonzero")),
            tabs,
        };
        snapshot.validate().expect("valid");
        snapshot
    }

    fn center(rect: Rect) -> Point {
        Point {
            x: rect.x + rect.width / 2.0,
            y: rect.y + rect.height / 2.0,
        }
    }

    #[test]
    fn the_bar_paints_its_surface_and_active_tab_roles() {
        let snapshot = snapshot(3, 2);
        let model = ChromeModel {
            snapshot: &snapshot,
            width: 800.0,
        };
        let list = render(&model, &LIGHT);
        assert!(matches!(
            list.items.first(),
            Some(DisplayItem::SolidColor { color, .. }) if *color == LIGHT.surface2
        ));
        assert!(
            list.items.iter().any(|item| matches!(
                item,
                DisplayItem::SolidColor { color, .. } if *color == LIGHT.surface3
            )),
            "the active tab paints surface 3"
        );
        assert!(
            list.items.iter().any(|item| matches!(
                item,
                DisplayItem::Text { text, .. } if text == "Tab 2"
            )),
            "tab titles are painted"
        );
    }

    #[test]
    fn presses_resolve_to_the_typed_commands() {
        let snapshot = snapshot(3, 2);
        let model = ChromeModel {
            snapshot: &snapshot,
            width: 800.0,
        };
        let geometry = geometry(&model);

        assert_eq!(
            command_at(&model, center(geometry.tabs[0].rect)),
            Some(ShellCommand::ActivateTab {
                tab: TabId::new(1).expect("nonzero")
            }),
            "an inactive tab activates"
        );
        assert_eq!(
            command_at(&model, center(geometry.tabs[1].rect)),
            Some(ShellCommand::OpenCommandField {
                tab: Some(TabId::new(2).expect("nonzero"))
            }),
            "the active tab opens the command field"
        );
        assert_eq!(
            command_at(&model, center(geometry.tabs[1].close)),
            Some(ShellCommand::CloseTab {
                tab: TabId::new(2).expect("nonzero")
            }),
            "the close region wins over its tab"
        );
        assert_eq!(
            command_at(&model, center(geometry.new_tab)),
            Some(ShellCommand::NewTab)
        );
        assert_eq!(
            command_at(&model, center(geometry.reload)),
            Some(ShellCommand::Reload {
                tab: TabId::new(2).expect("nonzero")
            })
        );
        assert_eq!(
            command_at(&model, Point { x: 5.0, y: 100.0 }),
            None,
            "below the bar is the page's territory"
        );
    }

    #[test]
    fn a_single_tab_shows_the_site_pill_that_opens_the_command_field() {
        let snapshot = snapshot(1, 1);
        let model = ChromeModel {
            snapshot: &snapshot,
            width: 800.0,
        };
        let geometry = geometry(&model);
        assert!(geometry.tabs.is_empty());
        let pill = geometry.site_pill.expect("pill exists");
        assert!(
            pill.width <= tokens::SITE_PILL_MAX_WIDTH,
            "the pill respects Nova's 420px cap"
        );
        assert_eq!(
            command_at(&model, center(pill)),
            Some(ShellCommand::OpenCommandField {
                tab: Some(TabId::new(1).expect("nonzero"))
            })
        );
    }

    #[test]
    fn the_palette_shows_placeholder_then_input_with_cursor() {
        let empty = render_palette(1000.0, 700.0, "", &LIGHT);
        assert!(empty.items.iter().any(|item| matches!(
            item,
            DisplayItem::Text { text, .. } if text.contains("Search the web")
        )));
        let typed = render_palette(1000.0, 700.0, "notes.html", &LIGHT);
        assert!(typed.items.iter().any(|item| matches!(
            item,
            DisplayItem::Text { text, .. } if text == "notes.html_"
        )));
    }
}
