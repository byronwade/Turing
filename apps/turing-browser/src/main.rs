// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Research-maturity windowed browser laboratory.
//!
//! This binary presents the `turing-engine` pipeline in a native window: it
//! loads an HTML file (or the built-in home page), lets the engine parse,
//! script, style, lay out, and paint it, and routes pointer input back through
//! the engine's epoch-guarded hit testing.
//!
//! # What this is not
//!
//! Not the product shell. The product toolkit selection (`ADR-0014`) is an
//! open owner decision with a required bake-off (`WP-004`); this window is the
//! laboratory presenter accepted in
//! `docs/research/graphics-foundation-decision-2026-07.md`, and `winit` plus
//! `softbuffer` appear here — and nowhere else in the workspace — under that
//! record. Everything above the last blit is engine-owned; replacing the
//! presenter touches this file only.
//!
//! Not a hostile-input boundary. It reads the file the user names on the
//! command line. There is no network, no untrusted navigation, and no claim
//! of sandboxing — the process boundary work lives in `turing-kernel` and is
//! not wired to this laboratory.

#![forbid(unsafe_code)]

use std::env;
use std::num::NonZeroU32;
use std::path::PathBuf;
use std::process::ExitCode;
use std::rc::Rc;

use turing_dom::Event;
use turing_engine::Page;
use turing_layout::Point;
use winit::application::ApplicationHandler;
use winit::dpi::{LogicalSize, PhysicalPosition};
use winit::event::{ElementState, MouseButton, WindowEvent};
use winit::event_loop::{ActiveEventLoop, ControlFlow, EventLoop};
use winit::keyboard::{Key, NamedKey};
use winit::window::{Window, WindowAttributes, WindowId};

/// The page shown when no file is named: a self-describing demonstration that
/// exercises text, styles, script mutation at load, and hit-testable regions.
const HOME: &str = include_str!("../home.html");

struct Browser {
    source: PageSource,
    page: Page,
    window: Option<Rc<Window>>,
    surface: Option<softbuffer::Surface<Rc<Window>, Rc<Window>>>,
    cursor: PhysicalPosition<f64>,
}

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
}

const INITIAL_WIDTH: f64 = 800.0;
const INITIAL_HEIGHT: f64 = 600.0;

impl Browser {
    fn new(source: PageSource) -> Result<Self, String> {
        let html = source.read()?;
        #[allow(clippy::cast_possible_truncation)]
        let page = Page::load(&html, INITIAL_WIDTH as f32)
            .map_err(|error| format!("page refused to load: {error}"))?;
        Ok(Self {
            source,
            page,
            window: None,
            surface: None,
            cursor: PhysicalPosition::new(0.0, 0.0),
        })
    }

    fn reload(&mut self) {
        let width = self.viewport_width();
        match self
            .source
            .read()
            .and_then(|html| Page::load(&html, width).map_err(|error| error.to_string()))
        {
            Ok(page) => {
                self.page = page;
                self.sync_title();
                self.request_redraw();
            }
            // A failed reload keeps the last good page. The refusal is
            // reported, not swallowed: the title carries it too, so it is
            // visible without a console.
            Err(error) => {
                eprintln!("turing-browser: reload refused: {error}");
                if let Some(window) = &self.window {
                    window.set_title(&format!("Turing (reload refused: {error})"));
                }
            }
        }
    }

    #[allow(clippy::cast_precision_loss, clippy::cast_possible_truncation)]
    fn viewport_width(&self) -> f32 {
        match &self.window {
            Some(window) => window.inner_size().width as f32,
            None => INITIAL_WIDTH as f32,
        }
    }

    fn sync_title(&self) {
        if let Some(window) = &self.window {
            let title = match self.page.title() {
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

    /// Paints the page into the softbuffer surface.
    ///
    /// The engine's canvas is the source of truth; this function only packs
    /// its opaque sRGB pixels into the presenter's `0RGB` words. Engine
    /// coordinates are CSS pixels at scale 1, so a physical pixel is a CSS
    /// pixel here; high-DPI scaling is presenter work the lab does not do.
    fn redraw(&mut self) {
        let (Some(window), Some(surface)) = (&self.window, &mut self.surface) else {
            return;
        };
        let size = window.inner_size();
        let (Some(width), Some(height)) =
            (NonZeroU32::new(size.width), NonZeroU32::new(size.height))
        else {
            return; // A minimised window has no surface to paint.
        };
        if surface.resize(width, height).is_err() {
            eprintln!("turing-browser: surface resize failed; skipping frame");
            return;
        }

        let canvas = match self.page.render(size.width as usize, size.height as usize) {
            Ok(canvas) => canvas,
            Err(error) => {
                eprintln!("turing-browser: render refused: {error}");
                return;
            }
        };

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
        let point = Point {
            x: self.cursor.x as f32,
            y: self.cursor.y as f32,
        };
        match self.page.target_at(point) {
            Ok(Some(node)) => {
                let name = self
                    .page
                    .dom()
                    .document()
                    .element_name(node)
                    .unwrap_or("#text")
                    .to_owned();
                let id = self
                    .page
                    .dom()
                    .document()
                    .attribute_of(node, "id")
                    .map(|id| format!("#{id}"))
                    .unwrap_or_default();
                println!("clicked <{name}{id}> at {:.0},{:.0}", point.x, point.y);
            }
            Ok(None) => println!("clicked background at {:.0},{:.0}", point.x, point.y),
            Err(error) => eprintln!("turing-browser: hit test refused: {error}"),
        }
        match self.page.dispatch_at(point, &Event::new("click")) {
            Ok(_) => self.request_redraw(),
            Err(error) => eprintln!("turing-browser: dispatch refused: {error}"),
        }
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
        _window: WindowId,
        event: WindowEvent,
    ) {
        match event {
            WindowEvent::CloseRequested => event_loop.exit(),
            WindowEvent::RedrawRequested => self.redraw(),
            WindowEvent::Resized(size) => {
                #[allow(clippy::cast_precision_loss)]
                let width = size.width as f32;
                if let Err(error) = self.page.resize(width) {
                    eprintln!("turing-browser: relayout refused: {error}");
                }
                self.request_redraw();
            }
            WindowEvent::CursorMoved { position, .. } => self.cursor = position,
            WindowEvent::MouseInput {
                state: ElementState::Pressed,
                button: MouseButton::Left,
                ..
            } => self.click(),
            WindowEvent::KeyboardInput { event, .. }
                if event.state == ElementState::Pressed
                    && event.logical_key == Key::Named(NamedKey::F5) =>
            {
                self.reload();
            }
            _ => {}
        }
    }
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
