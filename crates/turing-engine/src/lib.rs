// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! End-to-end composition of the engine crates.
//!
//! Every stage of the pipeline exists as its own crate with its own contract:
//! `turing-html` parses, `turing-dom` tracks liveness, `turing-css` cascades,
//! `turing-layout` positions, `turing-raster` paints, `turing-js` executes,
//! `turing-webidl` binds, and `turing-input` routes. What did not exist until
//! this crate is the composition — one type that owns a page and keeps the
//! stages consistent with each other as the document changes.
//!
//! # What [`Page`] guarantees
//!
//! A `Page` holds a parsed document together with the layout computed from it,
//! and every path that can mutate the document — running the page's scripts,
//! dispatching an input event — ends by re-running layout when the document's
//! epoch advanced. The hit router is rebuilt with the fresh layout at the same
//! time, so the staleness refusal in `turing-input` is an invariant here, not
//! a recoverable error: routing against outdated geometry is unrepresentable
//! rather than merely detected.
//!
//! # What this crate refuses to hide
//!
//! Each stage's refusals pass through unchanged inside [`EngineError`]. A page
//! whose stylesheet uses an unimplemented colour notation, or whose script
//! uses unsupported syntax, fails loudly at load — pretending a stage
//! succeeded is how a lab result quietly stops meaning anything.

#![forbid(unsafe_code)]

use core::fmt;

use turing_css::{CssError, Stylesheet};
use turing_dom::{Dispatch, Dom, DomError, Event};
use turing_gc::Bindings;
use turing_html::tree::{Document, NodeData, NodeId, TreeBuilder, TreeError};
use turing_html::{Tokenizer, TokenizerError};
use turing_input::{HitRouter, InputError};
use turing_js::{Host, JsError, Program, Value, Vm, compile};
use turing_layout::{
    DisplayList, LayoutBox, LayoutError, Point, TextMetrics, build_display_list, layout,
};
use turing_raster::{Canvas, RasterError, rasterize};
use turing_webidl::DomHost;

/// Wraps a [`DomHost`] with a small, host-persisted store for a minimal
/// component runtime's hook state (`__hookState`/`__hookSet`), on top of
/// the DOM operations `DomHost` already provides.
///
/// # Why this lives outside the VM's own heap
///
/// [`Vm::call`] and [`Vm::run_with_host`] each start a fresh heap; a value a
/// script allocates during one call (an object, array, or closure) does not
/// survive into the next separate call. A component's state, though, must
/// survive from the render that creates it to a later click's handler and
/// the re-render that follows — so it cannot live in anything the VM
/// allocates. It lives here instead, in a plain `Vec` owned by [`Page`]
/// across every call, addressed by an explicit slot index the script
/// itself provides (rather than an auto-incrementing per-render cursor,
/// which this minimal runtime does not implement).
///
/// # Why only primitive values are accepted
///
/// [`Value::Object`], [`Value::Array`], and [`Value::Closure`] are handles
/// into that same short-lived per-call heap. Persisting one here would let
/// a later call read a handle whose heap no longer exists — exactly the
/// dangling-reference hazard this workspace's collector design otherwise
/// prevents by construction. Refused with a typed host-operation failure
/// rather than stored, so a component that tries to hold richer state in a
/// hook finds out immediately, not from a future call reading corrupt data.
struct HookHost<'a, 'dom> {
    dom_host: DomHost<'dom>,
    hook_state: &'a mut Vec<Value>,
}

impl<'a, 'dom> HookHost<'a, 'dom> {
    fn new(dom_host: DomHost<'dom>, hook_state: &'a mut Vec<Value>) -> Self {
        let mut dom_host = dom_host;
        dom_host.register_extra("Hooks", "__hookState", 2);
        dom_host.register_extra("Hooks", "__hookSet", 2);
        Self {
            dom_host,
            hook_state,
        }
    }

    /// Reads `index` as a non-negative slot number.
    fn slot(value: &Value) -> Result<usize, String> {
        let Value::Number(index) = value else {
            return Err(format!("expected a hook slot index, got {value}"));
        };
        if *index < 0.0 || index.fract() != 0.0 {
            return Err(format!("{index} is not a hook slot index"));
        }
        #[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
        Ok(*index as usize)
    }

    /// Refuses a value that would dangle once this call's heap is gone —
    /// see this type's own doc comment for why only primitives are safe to
    /// persist here.
    fn primitive_or_refuse(value: &Value) -> Result<Value, String> {
        match value {
            Value::Object(_) | Value::Array(_) | Value::Closure(_) | Value::Function(_) => {
                Err(format!(
                    "hook state can only hold a primitive value (a number, string, boolean, \
                     null, or undefined); {value} references this call's own heap, which will \
                     no longer exist by the next call that reads it"
                ))
            }
            primitive => Ok(primitive.clone()),
        }
    }
}

impl Host for HookHost<'_, '_> {
    fn bindings(&self) -> &Bindings {
        self.dom_host.bindings()
    }

    fn invoke(
        &mut self,
        interface: &str,
        name: &str,
        arguments: &[Value],
    ) -> Result<Value, String> {
        match name {
            "__hookState" => {
                let slot = Self::slot(&arguments[0])?;
                let initial = Self::primitive_or_refuse(&arguments[1])?;
                if slot >= self.hook_state.len() {
                    self.hook_state.resize(slot + 1, Value::Undefined);
                }
                if self.hook_state[slot] == Value::Undefined {
                    self.hook_state[slot] = initial.clone();
                    Ok(initial)
                } else {
                    Ok(self.hook_state[slot].clone())
                }
            }
            "__hookSet" => {
                let slot = Self::slot(&arguments[0])?;
                let value = Self::primitive_or_refuse(&arguments[1])?;
                if slot >= self.hook_state.len() {
                    self.hook_state.resize(slot + 1, Value::Undefined);
                }
                self.hook_state[slot] = value;
                Ok(Value::Undefined)
            }
            _ => self.dom_host.invoke(interface, name, arguments),
        }
    }
}

/// A stage refusal, passed through from the crate that owns the contract.
#[derive(Clone, Debug, PartialEq)]
pub enum EngineError {
    Tokenize(TokenizerError),
    Tree(TreeError),
    Css(CssError),
    Layout(LayoutError),
    Dom(DomError),
    Input(InputError),
    Raster(RasterError),
    Script(JsError),
}

impl fmt::Display for EngineError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Tokenize(error) => write!(formatter, "tokenizer: {error}"),
            Self::Tree(error) => write!(formatter, "tree builder: {error}"),
            Self::Css(error) => write!(formatter, "css: {error}"),
            Self::Layout(error) => write!(formatter, "layout: {error}"),
            Self::Dom(error) => write!(formatter, "dom: {error}"),
            Self::Input(error) => write!(formatter, "input: {error}"),
            Self::Raster(error) => write!(formatter, "raster: {error}"),
            Self::Script(error) => write!(formatter, "script: {error}"),
        }
    }
}

impl std::error::Error for EngineError {}

macro_rules! from_stage {
    ($variant:ident, $error:ty) => {
        impl From<$error> for EngineError {
            fn from(error: $error) -> Self {
                Self::$variant(error)
            }
        }
    };
}

from_stage!(Tokenize, TokenizerError);
from_stage!(Tree, TreeError);
from_stage!(Css, CssError);
from_stage!(Layout, LayoutError);
from_stage!(Dom, DomError);
from_stage!(Input, InputError);
from_stage!(Raster, RasterError);
from_stage!(Script, JsError);

/// A loaded page: document, styles, layout, and input routing, kept coherent.
#[derive(Debug)]
pub struct Page {
    dom: Dom,
    sheet: Stylesheet,
    layout: LayoutBox,
    router: HitRouter,
    viewport_width: f32,
    metrics: TextMetrics,
    /// Compiled scripts, retained so listener functions registered through
    /// `addEventListener` stay callable after load.
    programs: Vec<Program>,
    /// The one node `:hover` rules currently match, if any. Lives on `Page`
    /// rather than being passed into each render call because it is a fact
    /// about the document's current state — the same role `scroll_y` plays
    /// for the caller-owned presenter, except hover changes what layout
    /// itself computes (a `:hover` rule can change a box's size), not only
    /// what paints, so it has to survive from `set_hovered` through to the
    /// next `relayout` rather than being a paint-time parameter.
    hovered: Option<NodeId>,
    /// A minimal component runtime's hook state (`__hookState`/`__hookSet`),
    /// addressed by an explicit slot index — see `HookHost` for why this
    /// cannot live in anything the script's own VM heap allocates.
    hook_state: Vec<Value>,
}

impl Page {
    /// Parses `html`, runs its `<script>` elements, and lays it out at
    /// `viewport_width` CSS pixels.
    ///
    /// Styles come from the document's `<style>` elements, concatenated in
    /// document order — there is no network, so there is nothing else they
    /// could come from. Scripts run once, at load, in document order, against
    /// the live document; a script mutation is reflected in the layout this
    /// constructor returns.
    ///
    /// # Errors
    ///
    /// Any stage refusal, unchanged. A page that parses but styles with an
    /// unsupported notation, or scripts with unsupported syntax, is an error
    /// rather than a partially loaded page.
    pub fn load(html: &str, viewport_width: f32) -> Result<Self, EngineError> {
        let tokens = Tokenizer::new(html).tokenize()?.tokens;
        let document = TreeBuilder::new().build(&tokens)?;
        let sheet = Stylesheet::parse(&collect_element_text(&document, "style"))?;
        let scripts = collect_scripts(&document);

        let mut dom = Dom::new(document);
        let mut programs = Vec::new();
        let mut hook_state = Vec::new();
        for source in &scripts {
            let program = compile(source)?;
            let mut host = HookHost::new(DomHost::new(&mut dom), &mut hook_state);
            Vm::default().run_with_host(&program, &mut host)?;
            programs.push(program);
        }

        let metrics = TextMetrics::default();
        let layout = layout(dom.document(), &sheet, viewport_width, metrics, None)?;
        let router = HitRouter::new(&dom, layout.clone());
        Ok(Self {
            dom,
            sheet,
            layout,
            router,
            viewport_width,
            metrics,
            programs,
            hook_state,
            hovered: None,
        })
    }

    /// The page title, from the first `<title>` element's text.
    #[must_use]
    pub fn title(&self) -> Option<String> {
        let title = collect_element_text(self.dom.document(), "title");
        let trimmed = title.trim();
        if trimmed.is_empty() {
            None
        } else {
            Some(trimmed.to_owned())
        }
    }

    /// The current layout root.
    #[must_use]
    pub fn layout(&self) -> &LayoutBox {
        &self.layout
    }

    /// The live document.
    #[must_use]
    pub fn dom(&self) -> &Dom {
        &self.dom
    }

    /// Builds the current display list.
    #[must_use]
    pub fn display_list(&self) -> DisplayList {
        build_display_list(&self.layout)
    }

    /// Paints the current layout onto a canvas of the given pixel size.
    ///
    /// The canvas background is white, which is the initial value of the
    /// canvas surface; a page that wants another background styles its `body`.
    ///
    /// # Errors
    ///
    /// Returns the rasterizer's allocation refusal for an oversized canvas.
    pub fn render(&self, width: usize, height: usize) -> Result<Canvas, EngineError> {
        self.render_scrolled(width, height, 0.0)
    }

    /// Paints with the viewport scrolled `scroll_y` CSS pixels down the page.
    ///
    /// Scrolling is a paint-time translation: geometry stays in page
    /// coordinates, so layout, hit testing, and the mutation-epoch guard are
    /// untouched by where the viewport happens to be. The caller owns the
    /// mapping of window points to page points (add `scroll_y`) and the
    /// clamping of `scroll_y` against [`Self::content_height`].
    ///
    /// # Errors
    ///
    /// Returns the rasterizer's allocation refusal for an oversized canvas.
    pub fn render_scrolled(
        &self,
        width: usize,
        height: usize,
        scroll_y: f32,
    ) -> Result<Canvas, EngineError> {
        let background = turing_css::Color {
            red: 255,
            green: 255,
            blue: 255,
        };
        let mut list = self.display_list();
        if scroll_y != 0.0 {
            for item in &mut list.items {
                match item {
                    turing_layout::DisplayItem::SolidColor { rect, .. }
                    | turing_layout::DisplayItem::RoundedColor { rect, .. }
                    | turing_layout::DisplayItem::Text { rect, .. } => rect.y -= scroll_y,
                }
            }
        }
        Ok(rasterize(&list, width, height, background)?)
    }

    /// The full laid-out height of the page in CSS pixels, independent of the
    /// window. This is what scroll offsets clamp against.
    #[must_use]
    pub fn content_height(&self) -> f32 {
        self.layout.dimensions.margin_box().height
    }

    /// Re-lays the page out at a new viewport width.
    ///
    /// # Errors
    ///
    /// Returns the layout stage's refusal, unchanged.
    pub fn resize(&mut self, viewport_width: f32) -> Result<(), EngineError> {
        self.viewport_width = viewport_width;
        self.relayout()
    }

    /// The element at `point`, if any.
    ///
    /// # Errors
    ///
    /// Propagates the input stage's refusals. Staleness is prevented by
    /// construction — every mutating path relays out before returning — so a
    /// staleness error here is a bug in this crate, not a caller mistake.
    pub fn target_at(&self, point: Point) -> Result<Option<NodeId>, EngineError> {
        Ok(self.router.target_at(&self.dom, point)?)
    }

    /// Sets which element, if any, `:hover` rules should currently match,
    /// and re-lays out to apply it.
    ///
    /// A caller with a pointer typically calls `target_at` on every pointer
    /// move and passes the result straight here — this method does not call
    /// `target_at` itself, so a caller with its own idea of "hovered" (touch,
    /// keyboard focus standing in for hover, a synthetic test) can drive it
    /// directly. Relaying out even when the node is unchanged from before
    /// would be wasted work, so this is a no-op when `node` already matches
    /// the current hovered node.
    ///
    /// # Errors
    ///
    /// Returns the layout stage's refusal, unchanged.
    pub fn set_hovered(&mut self, node: Option<NodeId>) -> Result<(), EngineError> {
        if node == self.hovered {
            return Ok(());
        }
        self.hovered = node;
        self.relayout()
    }

    /// Dispatches `event` to the element at `point`, runs any script
    /// listeners the dispatch reports, then re-lays out if anything mutated
    /// the document.
    ///
    /// The DOM owns propagation: `addEventListener` registered each listener
    /// under its function's name, dispatch reports invocations in capture,
    /// target, and bubble order, and this method executes the named functions
    /// in exactly that order against the live document.
    ///
    /// Returns the dispatch record, or `None` when nothing was hit.
    ///
    /// # Errors
    ///
    /// Propagates dispatch, script, and layout refusals unchanged. A listener
    /// naming a function no script defined is a script error, not a silent
    /// no-op — the page registered something it does not have.
    pub fn dispatch_at(
        &mut self,
        point: Point,
        event: &Event,
    ) -> Result<Option<Dispatch>, EngineError> {
        let before = self.dom.epoch();
        let dispatch = self.router.dispatch_at(&self.dom, point, event)?;
        if let Some(record) = &dispatch {
            for invocation in &record.invocations {
                let target = self
                    .dom
                    .document()
                    .attribute_of(invocation.node, "id")
                    .unwrap_or_default()
                    .to_owned();
                self.call_listener(&invocation.listener, &event.kind, &target)?;
            }
        }
        if self.dom.epoch() != before {
            self.relayout()?;
        }
        Ok(dispatch)
    }

    /// Calls the named listener function from whichever retained script
    /// defines it.
    ///
    /// The event reaches script as plain values rather than an event object:
    /// a listener declaring one parameter receives the event kind, one
    /// declaring two also receives the target element's id (empty when the
    /// target has none). Zero parameters receives nothing. The interpreter's
    /// arity check is strict, so this passes exactly what the function
    /// declared — a three-parameter listener is refused rather than padded.
    fn call_listener(&mut self, name: &str, kind: &str, target: &str) -> Result<(), EngineError> {
        let found = self
            .programs
            .iter()
            .enumerate()
            .find_map(|(index, program)| {
                program
                    .functions
                    .iter()
                    .skip(1)
                    .find(|function| function.name == name)
                    .map(|function| (index, function.arity))
            });
        let Some((index, arity)) = found else {
            return Err(EngineError::Script(JsError::HostOperationFailed {
                name: "addEventListener".to_owned(),
                message: format!("no retained script defines the listener function {name:?}"),
            }));
        };
        let available = [
            turing_js::Value::String(kind.to_owned()),
            turing_js::Value::String(target.to_owned()),
        ];
        let Some(arguments) = available.get(..arity) else {
            return Err(EngineError::Script(JsError::HostOperationFailed {
                name: "addEventListener".to_owned(),
                message: format!(
                    "the listener {name:?} declares {arity} parameters; the event supplies                      at most two (kind, target id)"
                ),
            }));
        };
        let mut host = HookHost::new(DomHost::new(&mut self.dom), &mut self.hook_state);
        Vm::default().call(&self.programs[index], name, arguments.to_vec(), &mut host)?;
        Ok(())
    }

    /// Runs `source` against the live document, then re-lays out if it
    /// mutated anything.
    ///
    /// The embedder decides when script runs; the page keeps itself coherent
    /// afterwards. The compiled program is retained, so functions it defines
    /// are callable by listeners registered here or earlier.
    ///
    /// # Errors
    ///
    /// Propagates compile, runtime, and layout refusals unchanged.
    pub fn run_script(&mut self, source: &str) -> Result<turing_js::Value, EngineError> {
        let program = compile(source)?;
        let before = self.dom.epoch();
        let mut host = HookHost::new(DomHost::new(&mut self.dom), &mut self.hook_state);
        let value = Vm::default().run_with_host(&program, &mut host)?;
        self.programs.push(program);
        if self.dom.epoch() != before {
            self.relayout()?;
        }
        Ok(value)
    }

    /// Recomputes layout from the current document and rebuilds the router.
    fn relayout(&mut self) -> Result<(), EngineError> {
        self.layout = layout(
            self.dom.document(),
            &self.sheet,
            self.viewport_width,
            self.metrics,
            self.hovered,
        )?;
        self.router = HitRouter::new(&self.dom, self.layout.clone());
        Ok(())
    }
}

/// Concatenates the text children of every `name` element, in document order.
fn collect_element_text(document: &Document, name: &str) -> String {
    let mut collected = String::new();
    for index in 0..document.len() {
        let id = NodeId::from_index(index);
        if document.element_name(id) != Some(name) {
            continue;
        }
        for &child in &document.node(id).children {
            if let NodeData::Text(text) = &document.node(child).data {
                collected.push_str(text);
                collected.push('\n');
            }
        }
    }
    collected
}

/// The text of each `<script>` element, one entry per element, in document
/// order. Separate entries rather than one concatenation because each script
/// compiles alone: one script's syntax refusal should name that script, not
/// poison the sources around it.
fn collect_scripts(document: &Document) -> Vec<String> {
    let mut scripts = Vec::new();
    for index in 0..document.len() {
        let id = NodeId::from_index(index);
        if document.element_name(id) != Some("script") {
            continue;
        }
        let mut source = String::new();
        for &child in &document.node(id).children {
            if let NodeData::Text(text) = &document.node(child).data {
                source.push_str(text);
                source.push('\n');
            }
        }
        if !source.trim().is_empty() {
            scripts.push(source);
        }
    }
    scripts
}
