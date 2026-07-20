// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Research-maturity windowed browser laboratory with Nova chrome.
//!
//! This binary presents the `turing-engine` pipeline in a native window under
//! the Nova-designed chrome rendered by `turing-chrome`: a unified bar with a
//! tab strip, the active-tab-as-address-field interaction, a command palette
//! for typed navigation, and epoch-guarded input routing into the page.
//!
//! Chrome and page meet in exactly one place: the composed display list. The
//! page's items paint first (translated below the bar and by the scroll
//! offset), the chrome's items paint over them, and the palette paints last —
//! the reference rasterizer's paint order is the entire compositing model.
//!
//! # What this is not
//!
//! Not the product shell. The product toolkit selection (`ADR-0014`) is an
//! open owner decision with a required bake-off (`WP-004`); this window is the
//! laboratory presenter accepted in
//! `docs/research/graphics-foundation-decision-2026-07.md`, and `winit` plus
//! `softbuffer` appear here — and nowhere else in the workspace — under that
//! record.
//!
//! Not a hostile-input boundary. It reads files the user names. There is no
//! network, no untrusted navigation, and no claim of sandboxing.

#![forbid(unsafe_code)]

use std::env;
use std::num::NonZeroU32;
use std::path::PathBuf;
use std::process::ExitCode;
use std::rc::Rc;

use turing_chrome::{ChromeModel, Theme};
use turing_css::Color;
use turing_dom::Event;
use turing_engine::Page;
use turing_layout::{DisplayItem, DisplayList, Point};
use turing_raster::rasterize;
use turing_types::{ProfileId, SpaceId, TabId, ViewId, WindowId};
use turing_ui_model::{ShellCommand, ShellSnapshot, TabLifecycle, TabSummary};
use winit::application::ApplicationHandler;
use winit::dpi::{LogicalSize, PhysicalPosition};
use winit::event::{ElementState, MouseButton, MouseScrollDelta, WindowEvent};
use winit::event_loop::{ActiveEventLoop, ControlFlow, EventLoop};
use winit::keyboard::{Key, NamedKey};
use winit::window::{Window, WindowAttributes, WindowId as WinitWindowId};

/// The page shown in a fresh tab: a self-describing demonstration that
/// exercises text, styles, script mutation at load, and hit-testable regions.
const HOME: &str = include_str!("../home.html");

const INITIAL_WIDTH: f64 = 1100.0;
const INITIAL_HEIGHT: f64 = 720.0;

#[derive(Clone)]
enum PageSource {
    BuiltIn,
    File(PathBuf),
}

impl PageSource {
    fn read(&self) -> Result<String, String> {
        match self {
            Self::BuiltIn => Ok(HOME.to_owned()),
            Self::File(path) => std::fs::read_to_string(path)
                .map_err(|error| format!("cannot read {}: {error}", path.display())),
        }
    }

    fn display_url(&self) -> String {
        match self {
            // The empty address renders Nova's "Search or enter address"
            // placeholder, which is the honest label for the built-in page.
            Self::BuiltIn => String::new(),
            Self::File(path) => path.display().to_string(),
        }
    }
}

struct Tab {
    id: TabId,
    view: ViewId,
    source: PageSource,
    page: Page,
    scroll_y: f32,
}

struct Browser {
    tabs: Vec<Tab>,
    active: usize,
    next_identity: u64,
    snapshot_version: u64,
    theme: Theme,
    /// `Some(text)` while the command palette is open.
    palette: Option<String>,
    window: Option<Rc<Window>>,
    surface: Option<softbuffer::Surface<Rc<Window>, Rc<Window>>>,
    cursor: PhysicalPosition<f64>,
}

impl Browser {
    fn new(source: PageSource) -> Result<Self, String> {
        let mut browser = Self {
            tabs: Vec::new(),
            active: 0,
            next_identity: 1,
            snapshot_version: 0,
            // Nova's default app state is the light theme.
            theme: turing_chrome::LIGHT,
            palette: None,
            window: None,
            surface: None,
            cursor: PhysicalPosition::new(0.0, 0.0),
        };
        let tab = browser.open_tab(source)?;
        browser.tabs.push(tab);
        Ok(browser)
    }

    fn open_tab(&mut self, source: PageSource) -> Result<Tab, String> {
        let html = source.read()?;
        let page = Page::load(&html, self.page_width())
            .map_err(|error| format!("page refused to load: {error}"))?;
        let identity = self.next_identity;
        self.next_identity += 1;
        Ok(Tab {
            id: TabId::new(identity).map_err(|error| error.to_string())?,
            view: ViewId::new(identity).map_err(|error| error.to_string())?,
            source,
            page,
            scroll_y: 0.0,
        })
    }

    fn active_tab(&self) -> &Tab {
        &self.tabs[self.active]
    }

    fn active_tab_mut(&mut self) -> &mut Tab {
        &mut self.tabs[self.active]
    }

    #[allow(clippy::cast_precision_loss, clippy::cast_possible_truncation)]
    fn window_size(&self) -> (f32, f32) {
        match &self.window {
            Some(window) => {
                let size = window.inner_size();
                (size.width as f32, size.height as f32)
            }
            None => (INITIAL_WIDTH as f32, INITIAL_HEIGHT as f32),
        }
    }

    fn page_width(&self) -> f32 {
        self.window_size().0
    }

    /// The page viewport height: the window below the chrome bar.
    fn page_height(&self) -> f32 {
        (self.window_size().1 - turing_chrome::bar_height()).max(0.0)
    }

    /// The immutable presentation state the chrome renders from.
    fn snapshot(&mut self) -> ShellSnapshot {
        self.snapshot_version += 1;
        let snapshot = ShellSnapshot {
            version: self.snapshot_version,
            window: WindowId::new(1).expect("nonzero"),
            profile: ProfileId::new(1).expect("nonzero"),
            space: SpaceId::new(1).expect("nonzero"),
            active_tab: self.tabs.get(self.active).map(|tab| tab.id),
            tabs: self
                .tabs
                .iter()
                .map(|tab| TabSummary {
                    id: tab.id,
                    view: tab.view,
                    title: tab.page.title().unwrap_or_else(|| "New Tab".to_owned()),
                    display_url: tab.source.display_url(),
                    lifecycle: TabLifecycle::Active,
                    protects_unsaved_work: false,
                })
                .collect(),
        };
        debug_assert!(snapshot.validate().is_ok());
        snapshot
    }

    fn clamp_scroll(&mut self) {
        let viewport = self.page_height();
        let tab = self.active_tab_mut();
        let max = (tab.page.content_height() - viewport).max(0.0);
        tab.scroll_y = tab.scroll_y.clamp(0.0, max);
    }

    fn scroll_by(&mut self, delta: f32) {
        self.active_tab_mut().scroll_y -= delta;
        self.clamp_scroll();
        self.request_redraw();
    }

    fn navigate_active(&mut self, source: PageSource) {
        let width = self.page_width();
        match source
            .read()
            .and_then(|html| Page::load(&html, width).map_err(|error| error.to_string()))
        {
            Ok(page) => {
                let tab = self.active_tab_mut();
                tab.page = page;
                tab.source = source;
                tab.scroll_y = 0.0;
                self.sync_title();
            }
            // A refused navigation keeps the last good page and says so.
            Err(error) => {
                eprintln!("turing-browser: navigation refused: {error}");
                if let Some(window) = &self.window {
                    window.set_title(&format!("Turing (navigation refused: {error})"));
                }
            }
        }
        self.request_redraw();
    }

    fn reload_tab(&mut self, id: TabId) {
        if let Some(index) = self.tabs.iter().position(|tab| tab.id == id) {
            let previous = self.active;
            self.active = index;
            let source = self.active_tab().source.clone();
            self.navigate_active(source);
            self.active = previous;
        }
    }

    fn apply(&mut self, command: ShellCommand) {
        match command {
            ShellCommand::ActivateTab { tab } => {
                if let Some(index) = self.tabs.iter().position(|candidate| candidate.id == tab) {
                    self.active = index;
                    self.sync_title();
                }
            }
            ShellCommand::CloseTab { tab } => {
                if let Some(index) = self.tabs.iter().position(|candidate| candidate.id == tab) {
                    self.tabs.remove(index);
                    if self.tabs.is_empty() {
                        // A window with no tabs is a closed window.
                        match self.open_tab(PageSource::BuiltIn) {
                            Ok(fresh) => self.tabs.push(fresh),
                            Err(error) => {
                                eprintln!("turing-browser: {error}");
                            }
                        }
                    }
                    self.active = self.active.min(self.tabs.len().saturating_sub(1));
                    self.sync_title();
                }
            }
            ShellCommand::NewTab => match self.open_tab(PageSource::BuiltIn) {
                Ok(tab) => {
                    self.tabs.push(tab);
                    self.active = self.tabs.len() - 1;
                    self.sync_title();
                }
                Err(error) => eprintln!("turing-browser: {error}"),
            },
            ShellCommand::Reload { tab } => self.reload_tab(tab),
            ShellCommand::OpenCommandField { .. } => {
                self.palette = Some(String::new());
            }
            // Navigation arrives through the palette rather than this
            // command today; freeze, restore, and space switching have no
            // backing service yet.
            ShellCommand::Navigate { .. }
            | ShellCommand::FreezeTab { .. }
            | ShellCommand::RestoreTab { .. }
            | ShellCommand::ActivateSpace { .. } => {}
        }
        self.request_redraw();
    }

    fn sync_title(&self) {
        if let Some(window) = &self.window {
            let title = match self.tabs.get(self.active).and_then(|tab| tab.page.title()) {
                Some(title) if title != "Turing" => format!("{title} - Turing"),
                _ => "Turing".to_owned(),
            };
            window.set_title(&title);
        }
    }

    fn request_redraw(&self) {
        if let Some(window) = &self.window {
            window.request_redraw();
        }
    }

    /// Composes page, chrome, and palette into one display list.
    ///
    /// Paint order is the compositing model: the page first (translated below
    /// the bar and by scroll), the opaque bar over any page overflow, the
    /// palette over everything.
    fn compose(&mut self, window_width: f32, window_height: f32) -> DisplayList {
        let bar = turing_chrome::bar_height();

        let mut list = DisplayList::default();
        // The page viewport background is the theme's ink.
        list.items.push(DisplayItem::SolidColor {
            rect: turing_layout::Rect {
                x: 0.0,
                y: bar,
                width: window_width,
                height: window_height - bar,
            },
            color: self.theme.ink,
        });
        // Pages assume a white canvas; paint one exactly the page's height.
        let tab = self.active_tab();
        list.items.push(DisplayItem::SolidColor {
            rect: turing_layout::Rect {
                x: 0.0,
                y: bar - tab.scroll_y,
                width: window_width,
                height: tab.page.content_height().max(window_height - bar),
            },
            color: Color {
                red: 255,
                green: 255,
                blue: 255,
            },
        });
        let offset = bar - tab.scroll_y;
        for mut item in tab.page.display_list().items {
            match &mut item {
                DisplayItem::SolidColor { rect, .. } | DisplayItem::Text { rect, .. } => {
                    rect.y += offset;
                }
            }
            list.items.push(item);
        }

        let snapshot = self.snapshot();
        let model = ChromeModel {
            snapshot: &snapshot,
            width: window_width,
        };
        list.items
            .extend(turing_chrome::render(&model, &self.theme).items);

        if let Some(input) = &self.palette {
            list.items.extend(
                turing_chrome::render_palette(window_width, window_height, input, &self.theme)
                    .items,
            );
        }
        list
    }

    /// Paints one frame into the presenter surface.
    fn redraw(&mut self) {
        let Some(size) = self.window.as_ref().map(|window| window.inner_size()) else {
            return;
        };
        if NonZeroU32::new(size.width).is_none() || NonZeroU32::new(size.height).is_none() {
            return; // A minimised window has no surface to paint.
        }

        #[allow(clippy::cast_precision_loss)]
        let list = self.compose(size.width as f32, size.height as f32);
        let canvas = match rasterize(
            &list,
            size.width as usize,
            size.height as usize,
            self.theme.ink,
        ) {
            Ok(canvas) => canvas,
            Err(error) => {
                eprintln!("turing-browser: render refused: {error}");
                return;
            }
        };

        // The list is composed and rasterized; only now is the presenter
        // surface touched, which keeps the borrow of `self` sequential.
        let Some(surface) = self.surface.as_mut() else {
            return;
        };
        let (Some(width), Some(height)) =
            (NonZeroU32::new(size.width), NonZeroU32::new(size.height))
        else {
            return;
        };
        if surface.resize(width, height).is_err() {
            eprintln!("turing-browser: surface resize failed; skipping frame");
            return;
        }
        let Ok(mut buffer) = surface.buffer_mut() else {
            eprintln!("turing-browser: presenter buffer unavailable; skipping frame");
            return;
        };
        for (slot, pixel) in buffer.iter_mut().zip(canvas.pixels()) {
            *slot = (u32::from(pixel.red) << 16)
                | (u32::from(pixel.green) << 8)
                | u32::from(pixel.blue);
        }
        if buffer.present().is_err() {
            eprintln!("turing-browser: present failed; the frame was dropped");
        }
    }

    fn click(&mut self) {
        #[allow(clippy::cast_possible_truncation)]
        let window_point = Point {
            x: self.cursor.x as f32,
            y: self.cursor.y as f32,
        };

        // An open palette owns the pointer: any press closes it, which is
        // the flat-render stand-in for clicking the veil.
        if self.palette.is_some() {
            self.palette = None;
            self.request_redraw();
            return;
        }

        let bar = turing_chrome::bar_height();
        if window_point.y < bar {
            let snapshot = self.snapshot();
            let model = ChromeModel {
                snapshot: &snapshot,
                width: self.window_size().0,
            };
            if let Some(command) = turing_chrome::command_at(&model, window_point) {
                self.apply(command);
            }
            return;
        }

        // Window points map to page points by removing the bar and adding
        // the scroll offset; geometry stays in page coordinates throughout.
        let scroll = self.active_tab().scroll_y;
        let point = Point {
            x: window_point.x,
            y: window_point.y - bar + scroll,
        };
        let tab = self.active_tab_mut();
        match tab.page.target_at(point) {
            Ok(Some(node)) => {
                let document = tab.page.dom().document();
                let name = document.element_name(node).unwrap_or("#text").to_owned();
                let id = document
                    .attribute_of(node, "id")
                    .map(|id| format!("#{id}"))
                    .unwrap_or_default();
                println!("clicked <{name}{id}> at {:.0},{:.0}", point.x, point.y);
            }
            Ok(None) => println!("clicked background at {:.0},{:.0}", point.x, point.y),
            Err(error) => eprintln!("turing-browser: hit test refused: {error}"),
        }
        match tab.page.dispatch_at(point, &Event::new("click")) {
            Ok(_) => self.request_redraw(),
            Err(error) => eprintln!("turing-browser: dispatch refused: {error}"),
        }
    }

    /// Keyboard input while the palette is open: text entry, submit, dismiss.
    fn palette_key(&mut self, key: &Key) -> bool {
        let Some(input) = &mut self.palette else {
            return false;
        };
        match key {
            Key::Named(NamedKey::Escape) => {
                self.palette = None;
            }
            Key::Named(NamedKey::Backspace) => {
                input.pop();
            }
            Key::Named(NamedKey::Enter) => {
                let typed = input.trim().to_owned();
                self.palette = None;
                if !typed.is_empty() {
                    self.navigate_active(PageSource::File(PathBuf::from(typed)));
                }
            }
            Key::Named(NamedKey::Space) => input.push(' '),
            Key::Character(text) => input.push_str(text),
            _ => return true,
        }
        self.request_redraw();
        true
    }
}

impl ApplicationHandler for Browser {
    fn resumed(&mut self, event_loop: &ActiveEventLoop) {
        if self.window.is_some() {
            return;
        }
        let attributes = WindowAttributes::default()
            .with_title("Turing")
            .with_inner_size(LogicalSize::new(INITIAL_WIDTH, INITIAL_HEIGHT));
        let window = match event_loop.create_window(attributes) {
            Ok(window) => Rc::new(window),
            Err(error) => {
                eprintln!("turing-browser: no window: {error}");
                event_loop.exit();
                return;
            }
        };
        let context = match softbuffer::Context::new(Rc::clone(&window)) {
            Ok(context) => context,
            Err(error) => {
                eprintln!("turing-browser: no presenter context: {error}");
                event_loop.exit();
                return;
            }
        };
        match softbuffer::Surface::new(&context, Rc::clone(&window)) {
            Ok(surface) => self.surface = Some(surface),
            Err(error) => {
                eprintln!("turing-browser: no presenter surface: {error}");
                event_loop.exit();
                return;
            }
        }
        self.window = Some(window);
        self.sync_title();
        self.request_redraw();
    }

    fn window_event(
        &mut self,
        event_loop: &ActiveEventLoop,
        _window: WinitWindowId,
        event: WindowEvent,
    ) {
        match event {
            WindowEvent::CloseRequested => event_loop.exit(),
            WindowEvent::RedrawRequested => self.redraw(),
            WindowEvent::Resized(size) => {
                #[allow(clippy::cast_precision_loss)]
                let width = size.width as f32;
                for index in 0..self.tabs.len() {
                    if let Err(error) = self.tabs[index].page.resize(width) {
                        eprintln!("turing-browser: relayout refused: {error}");
                    }
                }
                self.clamp_scroll();
                self.request_redraw();
            }
            WindowEvent::MouseWheel { delta, .. } => {
                if self.palette.is_none() {
                    let pixels = match delta {
                        // One wheel line scrolls three text lines, the
                        // common platform default.
                        MouseScrollDelta::LineDelta(_, lines) => lines * 48.0,
                        #[allow(clippy::cast_possible_truncation)]
                        MouseScrollDelta::PixelDelta(position) => position.y as f32,
                    };
                    self.scroll_by(pixels);
                }
            }
            WindowEvent::CursorMoved { position, .. } => self.cursor = position,
            WindowEvent::MouseInput {
                state: ElementState::Pressed,
                button: MouseButton::Left,
                ..
            } => self.click(),
            WindowEvent::KeyboardInput { event, .. } if event.state == ElementState::Pressed => {
                if self.palette_key(&event.logical_key) {
                    return;
                }
                if event.logical_key == Key::Named(NamedKey::F5) {
                    let id = self.active_tab().id;
                    self.reload_tab(id);
                }
            }
            _ => {}
        }
    }
}

/// Renders one composed frame headlessly and writes it as a BMP.
///
/// This is the window minus the window: the same `compose` path the live
/// presenter paints, reproducible without a display, which makes it the
/// visual-regression artifact for the chrome.
fn screenshot(out: &str, source: PageSource, extra_tabs: usize) -> Result<(), String> {
    let mut browser = Browser::new(source)?;
    for _ in 0..extra_tabs {
        let tab = browser.open_tab(PageSource::BuiltIn)?;
        browser.tabs.push(tab);
    }
    #[allow(clippy::cast_possible_truncation)]
    let (width, height) = (INITIAL_WIDTH as f32, INITIAL_HEIGHT as f32);
    let list = browser.compose(width, height);
    #[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
    let canvas = rasterize(&list, width as usize, height as usize, browser.theme.ink)
        .map_err(|error| error.to_string())?;
    std::fs::write(out, turing_raster::encode_bmp(&canvas))
        .map_err(|error| format!("cannot write {out}: {error}"))?;
    println!("wrote {out}");
    Ok(())
}

fn run() -> Result<(), String> {
    let source = match env::args().nth(1).as_deref() {
        None => PageSource::BuiltIn,
        Some("--version") => {
            let identity = turing_build_info::BuildIdentity::current();
            println!(
                "turing-browser {} {:?} {}",
                identity.version,
                identity.maturity,
                identity.source_commit.unwrap_or("unversioned-source")
            );
            return Ok(());
        }
        Some("--screenshot") => {
            let out = env::args()
                .nth(2)
                .ok_or("usage: --screenshot <out.bmp> [page.html] [extra-tabs]")?;
            let source = env::args().nth(3).map_or(PageSource::BuiltIn, |path| {
                PageSource::File(PathBuf::from(path))
            });
            let extra = env::args()
                .nth(4)
                .map_or(Ok(0), |raw| raw.parse::<usize>())
                .map_err(|error| format!("extra-tabs: {error}"))?;
            return screenshot(&out, source, extra);
        }
        Some(path) => PageSource::File(PathBuf::from(path)),
    };

    let mut browser = Browser::new(source)?;
    let event_loop = EventLoop::new().map_err(|error| format!("no event loop: {error}"))?;
    // Wait rather than poll: this laboratory redraws on input and resize, and
    // an idle page should cost nothing.
    event_loop.set_control_flow(ControlFlow::Wait);
    event_loop
        .run_app(&mut browser)
        .map_err(|error| format!("event loop failed: {error}"))
}

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("turing-browser: {error}");
            ExitCode::FAILURE
        }
    }
}
