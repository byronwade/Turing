// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Turing-owned CSS parsing, selector matching, and cascade.
//!
//! This crate implements `WP-008` and `REQ-ENG-003`: parsing a stylesheet into
//! rules, matching selectors against a [`turing_html`] document, and resolving
//! the cascade into a computed declaration set per element. It is written from
//! the CSS Syntax, Selectors, and Cascade specifications and derives from no
//! existing browser engine, consistent with `ADR-0009` Option A.
//!
//! # Pipeline position
//!
//! HTML parsing produces a tree; this crate decides which declarations apply to
//! each node in that tree. It does not compute used values, resolve relative
//! units, perform inheritance of every property, or lay anything out. Those are
//! `WP-009`.
//!
//! # Deliberate limits
//!
//! Selector support covers the forms reachable from ordinary stylesheets: type,
//! universal, class, id, attribute presence and equality, descendant, child,
//! adjacent sibling, general sibling, and selector lists.
//!
//! Constructs that change which elements match, rather than merely adding
//! detail, return a typed error instead of a guess:
//!
//! - at-rules such as `@media` and `@supports`, whose conditions gate whole
//!   rule blocks;
//! - structural and functional pseudo-classes such as `:nth-child()`,
//!   `:not()`, `:is()`, and `:has()`;
//! - pseudo-elements such as `::before`, which generate boxes that do not
//!   correspond to DOM nodes.
//!
//! Silently ignoring any of these would apply a rule to the wrong elements,
//! which is worse than refusing, because the page would render confidently and
//! incorrectly.
//!
//! # Custom properties and `var()`
//!
//! `--name: value` declarations, and `var(--name)` / `var(--name, fallback)`
//! references, are parsed and resolved — see [`Declaration`]'s doc comment
//! for how a custom property is stored, and [`resolve_declarations`] for how
//! a reference is substituted following the same cascade and inheritance
//! rules any other property gets. The same refuse-rather-than-guess policy
//! applies here: a `var()` naming a custom property that is not declared
//! anywhere applicable, with no fallback, is
//! [`CssError::CustomPropertyUndefined`] rather than an empty or invented
//! value, and malformed `var()` syntax or fallback nesting past a bounded
//! depth are refused too, rather than parsed approximately.

#![forbid(unsafe_code)]

use core::fmt;

/// The tree this crate matches selectors against.
///
/// Selector matching needs four questions answered about a node and nothing
/// else. Expressing that as a trait rather than a concrete document type is
/// what lets this crate style a host's own tree: a game UI, a design tool, a
/// terminal renderer. The engine's own DOM is one implementation of it, behind
/// the `html` feature, not a requirement.
pub trait ElementTree {
    /// Node handle. Cheap to copy, because matching passes them constantly.
    type Node: Copy + Eq;

    /// Returns whether the node is an element rather than text or a comment.
    fn is_element(&self, node: Self::Node) -> bool;

    /// Returns the element's lowercased tag name.
    fn tag_name(&self, node: Self::Node) -> Option<&str>;

    /// Returns an attribute value by lowercased name.
    fn attribute(&self, node: Self::Node, name: &str) -> Option<&str>;

    /// Returns the parent node.
    fn parent(&self, node: Self::Node) -> Option<Self::Node>;

    /// Returns the nearest preceding sibling that is an element.
    fn previous_element_sibling(&self, node: Self::Node) -> Option<Self::Node>;
}

/// A construct this implementation does not model.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum CssError {
    /// An at-rule was encountered. Its condition gates a whole rule block.
    AtRuleUnsupported { name: String },
    /// A pseudo-class this implementation does not evaluate.
    PseudoClassUnsupported { name: String },
    /// A pseudo-element, which generates boxes without DOM nodes.
    PseudoElementUnsupported { name: String },
    /// A selector could not be parsed.
    MalformedSelector { text: String },
    /// A declaration block was not closed.
    UnterminatedBlock { offset: usize },
    /// A colour notation this implementation does not parse.
    ColorUnsupported { value: String },
    /// `var()` named a custom property that is not declared anywhere
    /// applicable to the element being resolved, and no fallback was given.
    CustomPropertyUndefined { name: String },
    /// A `var()` reference could not be parsed: no arguments, an unmatched
    /// parenthesis, or a first argument that is not a custom property name
    /// (it must start with `--`).
    CustomPropertySyntax { text: String },
    /// A `var()` fallback, or the chain of custom properties it resolves
    /// through, nested past the depth this implementation bounds recursion
    /// to (see the `MAX_VAR_NESTING` constant).
    CustomPropertyNestingTooDeep { text: String },
}

/// An opaque sRGB colour.
///
/// # Why this is parsed here
///
/// A display list carrying colours as unparsed CSS strings pushes colour
/// parsing into every painter that consumes one, and those implementations
/// diverge. Parsing once, in the layer that owns CSS values, means a painter
/// receives channels it can use directly and an invalid colour is reported
/// against the stylesheet that contains it rather than at paint time.
///
/// Opaque only. Alpha requires compositing rules — what a translucent colour
/// blends against depends on stacking order and group opacity — and a painter
/// that ignored alpha would silently render translucent content as solid.
#[derive(Clone, Copy, Debug, Default, Eq, PartialEq)]
pub struct Color {
    pub red: u8,
    pub green: u8,
    pub blue: u8,
}

impl Color {
    /// Parses a CSS colour value.
    ///
    /// Accepts `#rgb`, `#rrggbb`, `rgb()`/`rgba()`, `hsl()`/`hsla()`, and
    /// the complete CSS Color 4 named set.
    ///
    /// # Errors
    ///
    /// Returns [`CssError::ColorUnsupported`] for any other notation — `lab()`,
    /// `oklch()`, eight-digit hex, `currentColor` — and for any alpha below 1:
    /// this value layer is opaque, translucency is the compositing painter's
    /// domain, and a translucent colour silently flattened to opaque is a
    /// plausible wrong colour that no one notices.
    pub fn parse(value: &str) -> Result<Self, CssError> {
        let value = value.trim();
        let unsupported = || CssError::ColorUnsupported {
            value: value.to_string(),
        };

        if let Some(hex) = value.strip_prefix('#') {
            // Three digits expand by repeating each, so `#abc` is `#aabbcc`,
            // not `#0a0b0c`.
            let expanded = match hex.len() {
                3 => hex.chars().flat_map(|c| [c, c]).collect::<String>(),
                6 => hex.to_string(),
                _ => return Err(unsupported()),
            };
            let channel = |range: core::ops::Range<usize>| {
                u8::from_str_radix(&expanded[range], 16).map_err(|_| unsupported())
            };
            return Ok(Self {
                red: channel(0..2)?,
                green: channel(2..4)?,
                blue: channel(4..6)?,
            });
        }

        if let Some(rest) = value
            .strip_prefix("hsl(")
            .or_else(|| value.strip_prefix("hsla("))
        {
            let inner = rest.strip_suffix(')').ok_or_else(unsupported)?;
            let normalized = inner.replace([',', '/'], " ");
            let parts: Vec<&str> = normalized.split_whitespace().collect();
            let (channels, alpha) = match parts.len() {
                3 => (&parts[..3], None),
                4 => (&parts[..3], Some(parts[3])),
                _ => return Err(unsupported()),
            };
            if let Some(alpha) = alpha
                && !matches!(alpha, "1" | "1.0" | "100%")
            {
                return Err(unsupported());
            }
            // `"NaN"` and `"inf"` are both syntax `f32::from_str` accepts, so
            // either would otherwise count as *parsed*, not *unparseable* —
            // exactly the gap that let `hsl(NaN, 50%, 50%)` and
            // `hsl(0, NaN%, 50%)` silently resolve to a plausible-but-wrong
            // colour instead of refusing, the same failure mode this
            // parser's other refusals exist to prevent. `NaN` bypasses
            // `clamp` (which returns `NaN` unchanged for a `NaN` input) and
            // an infinite hue is not guaranteed correct through
            // `rem_euclid`, so both channels below are checked with
            // `is_finite` before being trusted for arithmetic.
            let hue_raw: f32 = channels[0]
                .strip_suffix("deg")
                .unwrap_or(channels[0])
                .parse()
                .map_err(|_| unsupported())?;
            if !hue_raw.is_finite() {
                return Err(unsupported());
            }
            let hue = hue_raw;
            let percent = |raw: &str| -> Result<f32, CssError> {
                let raw = raw.strip_suffix('%').ok_or_else(unsupported)?;
                let parsed: f32 = raw.parse().map_err(|_| unsupported())?;
                if !parsed.is_finite() {
                    return Err(unsupported());
                }
                Ok((parsed / 100.0).clamp(0.0, 1.0))
            };
            let saturation = percent(channels[1])?;
            let lightness = percent(channels[2])?;
            // The specification's HSL-to-RGB algorithm, verbatim.
            let chroma = (1.0 - 2.0f32.mul_add(lightness, -1.0).abs()) * saturation;
            let hue_prime = hue.rem_euclid(360.0) / 60.0;
            let secondary = chroma * (1.0 - (hue_prime % 2.0 - 1.0).abs());
            let (red, green, blue) = match hue_prime {
                h if h < 1.0 => (chroma, secondary, 0.0),
                h if h < 2.0 => (secondary, chroma, 0.0),
                h if h < 3.0 => (0.0, chroma, secondary),
                h if h < 4.0 => (0.0, secondary, chroma),
                h if h < 5.0 => (secondary, 0.0, chroma),
                _ => (chroma, 0.0, secondary),
            };
            let lightness_match = lightness - chroma / 2.0;
            #[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
            let channel = |v: f32| ((v + lightness_match) * 255.0).round().clamp(0.0, 255.0) as u8;
            return Ok(Self {
                red: channel(red),
                green: channel(green),
                blue: channel(blue),
            });
        }

        if let Some(rest) = value
            .strip_prefix("rgb(")
            .or_else(|| value.strip_prefix("rgba("))
        {
            let inner = rest.strip_suffix(')').ok_or_else(unsupported)?;
            // Commas, spaces, and the slash-alpha form all normalise to
            // whitespace separation.
            let normalized = inner.replace([',', '/'], " ");
            let parts: Vec<&str> = normalized.split_whitespace().collect();
            let (channels, alpha) = match parts.len() {
                3 => (&parts[..3], None),
                4 => (&parts[..3], Some(parts[3])),
                _ => return Err(unsupported()),
            };
            if let Some(alpha) = alpha
                && !matches!(alpha, "1" | "1.0" | "100%")
            {
                return Err(unsupported());
            }
            let channel = |raw: &str| -> Result<u8, CssError> {
                let scaled = if let Some(percent) = raw.strip_suffix('%') {
                    percent.parse::<f32>().map_err(|_| unsupported())? / 100.0 * 255.0
                } else {
                    raw.parse::<f32>().map_err(|_| unsupported())?
                };
                // `"NaN"` is syntax `f32::from_str` accepts, so it counts as
                // parsed, not unparseable — and `NaN` bypasses `clamp`
                // (which returns `NaN` unchanged for a `NaN` input) rather
                // than being brought into range by it. Without this check,
                // `rgb(NaN, 0, 0)` silently resolved to `rgb(0, 0, 0)` via
                // the saturating float-to-`u8` cast below, rather than being
                // refused the way any other unparseable channel already is.
                if !scaled.is_finite() {
                    return Err(unsupported());
                }
                // The specification clamps out-of-range channels rather than
                // refusing them.
                #[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
                Ok(scaled.clamp(0.0, 255.0).round() as u8)
            };
            return Ok(Self {
                red: channel(channels[0])?,
                green: channel(channels[1])?,
                blue: channel(channels[2])?,
            });
        }

        // The complete CSS Color 4 named-colour set — one hundred and
        // forty-eight names, generated mechanically from the specification's
        // own table rather than transcribed by hand, because a mistyped
        // channel renders a plausible wrong colour that nobody reports.
        // Names sharing a value (the gray/grey pairs, aqua/cyan,
        // fuchsia/magenta) share an arm.
        let named = match value.to_ascii_lowercase().as_str() {
            "aliceblue" => (240, 248, 255),
            "antiquewhite" => (250, 235, 215),
            "aqua" | "cyan" => (0, 255, 255),
            "aquamarine" => (127, 255, 212),
            "azure" => (240, 255, 255),
            "beige" => (245, 245, 220),
            "bisque" => (255, 228, 196),
            "black" => (0, 0, 0),
            "blanchedalmond" => (255, 235, 205),
            "blue" => (0, 0, 255),
            "blueviolet" => (138, 43, 226),
            "brown" => (165, 42, 42),
            "burlywood" => (222, 184, 135),
            "cadetblue" => (95, 158, 160),
            "chartreuse" => (127, 255, 0),
            "chocolate" => (210, 105, 30),
            "coral" => (255, 127, 80),
            "cornflowerblue" => (100, 149, 237),
            "cornsilk" => (255, 248, 220),
            "crimson" => (220, 20, 60),
            "darkblue" => (0, 0, 139),
            "darkcyan" => (0, 139, 139),
            "darkgoldenrod" => (184, 134, 11),
            "darkgray" | "darkgrey" => (169, 169, 169),
            "darkgreen" => (0, 100, 0),
            "darkkhaki" => (189, 183, 107),
            "darkmagenta" => (139, 0, 139),
            "darkolivegreen" => (85, 107, 47),
            "darkorange" => (255, 140, 0),
            "darkorchid" => (153, 50, 204),
            "darkred" => (139, 0, 0),
            "darksalmon" => (233, 150, 122),
            "darkseagreen" => (143, 188, 143),
            "darkslateblue" => (72, 61, 139),
            "darkslategray" | "darkslategrey" => (47, 79, 79),
            "darkturquoise" => (0, 206, 209),
            "darkviolet" => (148, 0, 211),
            "deeppink" => (255, 20, 147),
            "deepskyblue" => (0, 191, 255),
            "dimgray" | "dimgrey" => (105, 105, 105),
            "dodgerblue" => (30, 144, 255),
            "firebrick" => (178, 34, 34),
            "floralwhite" => (255, 250, 240),
            "forestgreen" => (34, 139, 34),
            "fuchsia" | "magenta" => (255, 0, 255),
            "gainsboro" => (220, 220, 220),
            "ghostwhite" => (248, 248, 255),
            "gold" => (255, 215, 0),
            "goldenrod" => (218, 165, 32),
            "gray" | "grey" => (128, 128, 128),
            "green" => (0, 128, 0),
            "greenyellow" => (173, 255, 47),
            "honeydew" => (240, 255, 240),
            "hotpink" => (255, 105, 180),
            "indianred" => (205, 92, 92),
            "indigo" => (75, 0, 130),
            "ivory" => (255, 255, 240),
            "khaki" => (240, 230, 140),
            "lavender" => (230, 230, 250),
            "lavenderblush" => (255, 240, 245),
            "lawngreen" => (124, 252, 0),
            "lemonchiffon" => (255, 250, 205),
            "lightblue" => (173, 216, 230),
            "lightcoral" => (240, 128, 128),
            "lightcyan" => (224, 255, 255),
            "lightgoldenrodyellow" => (250, 250, 210),
            "lightgray" | "lightgrey" => (211, 211, 211),
            "lightgreen" => (144, 238, 144),
            "lightpink" => (255, 182, 193),
            "lightsalmon" => (255, 160, 122),
            "lightseagreen" => (32, 178, 170),
            "lightskyblue" => (135, 206, 250),
            "lightslategray" | "lightslategrey" => (119, 136, 153),
            "lightsteelblue" => (176, 196, 222),
            "lightyellow" => (255, 255, 224),
            "lime" => (0, 255, 0),
            "limegreen" => (50, 205, 50),
            "linen" => (250, 240, 230),
            "maroon" => (128, 0, 0),
            "mediumaquamarine" => (102, 205, 170),
            "mediumblue" => (0, 0, 205),
            "mediumorchid" => (186, 85, 211),
            "mediumpurple" => (147, 112, 219),
            "mediumseagreen" => (60, 179, 113),
            "mediumslateblue" => (123, 104, 238),
            "mediumspringgreen" => (0, 250, 154),
            "mediumturquoise" => (72, 209, 204),
            "mediumvioletred" => (199, 21, 133),
            "midnightblue" => (25, 25, 112),
            "mintcream" => (245, 255, 250),
            "mistyrose" => (255, 228, 225),
            "moccasin" => (255, 228, 181),
            "navajowhite" => (255, 222, 173),
            "navy" => (0, 0, 128),
            "oldlace" => (253, 245, 230),
            "olive" => (128, 128, 0),
            "olivedrab" => (107, 142, 35),
            "orange" => (255, 165, 0),
            "orangered" => (255, 69, 0),
            "orchid" => (218, 112, 214),
            "palegoldenrod" => (238, 232, 170),
            "palegreen" => (152, 251, 152),
            "paleturquoise" => (175, 238, 238),
            "palevioletred" => (219, 112, 147),
            "papayawhip" => (255, 239, 213),
            "peachpuff" => (255, 218, 185),
            "peru" => (205, 133, 63),
            "pink" => (255, 192, 203),
            "plum" => (221, 160, 221),
            "powderblue" => (176, 224, 230),
            "purple" => (128, 0, 128),
            "rebeccapurple" => (102, 51, 153),
            "red" => (255, 0, 0),
            "rosybrown" => (188, 143, 143),
            "royalblue" => (65, 105, 225),
            "saddlebrown" => (139, 69, 19),
            "salmon" => (250, 128, 114),
            "sandybrown" => (244, 164, 96),
            "seagreen" => (46, 139, 87),
            "seashell" => (255, 245, 238),
            "sienna" => (160, 82, 45),
            "silver" => (192, 192, 192),
            "skyblue" => (135, 206, 235),
            "slateblue" => (106, 90, 205),
            "slategray" | "slategrey" => (112, 128, 144),
            "snow" => (255, 250, 250),
            "springgreen" => (0, 255, 127),
            "steelblue" => (70, 130, 180),
            "tan" => (210, 180, 140),
            "teal" => (0, 128, 128),
            "thistle" => (216, 191, 216),
            "tomato" => (255, 99, 71),
            "turquoise" => (64, 224, 208),
            "violet" => (238, 130, 238),
            "wheat" => (245, 222, 179),
            "white" => (255, 255, 255),
            "whitesmoke" => (245, 245, 245),
            "yellow" => (255, 255, 0),
            "yellowgreen" => (154, 205, 50),
            _ => return Err(unsupported()),
        };
        Ok(Self {
            red: named.0,
            green: named.1,
            blue: named.2,
        })
    }
}

impl fmt::Display for CssError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::AtRuleUnsupported { name } => write!(
                formatter,
                "at-rule @{name} is not implemented; its condition gates a whole rule block"
            ),
            Self::PseudoClassUnsupported { name } => write!(
                formatter,
                "pseudo-class :{name} is not implemented; ignoring it would match the wrong elements"
            ),
            Self::PseudoElementUnsupported { name } => write!(
                formatter,
                "pseudo-element ::{name} is not implemented; it generates boxes without DOM nodes"
            ),
            Self::MalformedSelector { text } => {
                write!(formatter, "malformed selector: {text}")
            }
            Self::UnterminatedBlock { offset } => {
                write!(formatter, "unterminated declaration block at byte {offset}")
            }
            Self::ColorUnsupported { value } => write!(
                formatter,
                "colour {value} is not parsed here; defaulting it would paint a \
                 plausible wrong colour rather than report a gap"
            ),
            Self::CustomPropertyUndefined { name } => write!(
                formatter,
                "custom property {name} is referenced by var() but is not declared \
                 anywhere this element inherits from, and no fallback was given; \
                 inventing a value here would be a plausible wrong value nobody notices"
            ),
            Self::CustomPropertySyntax { text } => write!(
                formatter,
                "var() reference in `{text}` could not be parsed: it needs a \
                 custom property name starting with `--`, and matching parentheses"
            ),
            Self::CustomPropertyNestingTooDeep { text } => write!(
                formatter,
                "var() in `{text}` nests custom property references past the \
                 depth this implementation bounds recursion to; this is refused \
                 rather than risking runaway recursion on a cyclic definition"
            ),
        }
    }
}

/// How two compound selectors are related.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Combinator {
    /// `A B` — B is any descendant of A.
    Descendant,
    /// `A > B` — B is a direct child of A.
    Child,
    /// `A + B` — B immediately follows A among siblings.
    NextSibling,
    /// `A ~ B` — B follows A among siblings.
    SubsequentSibling,
}

/// A single condition within a compound selector.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum SimpleSelector {
    /// `*`
    Universal,
    /// `div`
    Type(String),
    /// `.name`
    Class(String),
    /// `#name`
    Id(String),
    /// `[name]`
    AttributePresent(String),
    /// `[name="value"]`
    AttributeEquals { name: String, value: String },
    /// `:hover` — matches when the caller-supplied hovered node is this
    /// element. The only pseudo-class this crate evaluates; every other one
    /// is refused at parse time rather than silently ignored.
    Hover,
}

/// Conditions that must all hold for one element.
#[derive(Clone, Debug, Default, Eq, PartialEq)]
pub struct Compound {
    /// Conditions in source order.
    pub parts: Vec<SimpleSelector>,
}

/// A full selector: compounds joined by combinators, read left to right.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Selector {
    /// The rightmost compound, which the candidate element must match.
    pub subject: Compound,
    /// Ancestor or sibling constraints, nearest first.
    pub ancestors: Vec<(Combinator, Compound)>,
}

/// Selector specificity as the (id, class, type) triple the cascade compares.
#[derive(Clone, Copy, Debug, Default, Eq, Ord, PartialEq, PartialOrd)]
pub struct Specificity {
    /// Count of id conditions.
    pub ids: u32,
    /// Count of class and attribute conditions.
    pub classes: u32,
    /// Count of type conditions.
    pub types: u32,
}

impl Selector {
    /// Returns this selector's specificity.
    #[must_use]
    pub fn specificity(&self) -> Specificity {
        let mut total = Specificity::default();
        let mut count = |compound: &Compound| {
            for part in &compound.parts {
                match part {
                    SimpleSelector::Id(_) => total.ids += 1,
                    SimpleSelector::Class(_)
                    | SimpleSelector::AttributePresent(_)
                    | SimpleSelector::AttributeEquals { .. }
                    | SimpleSelector::Hover => total.classes += 1,
                    SimpleSelector::Type(_) => total.types += 1,
                    SimpleSelector::Universal => {}
                }
            }
        };
        count(&self.subject);
        for (_, compound) in &self.ancestors {
            count(compound);
        }
        total
    }
}

/// A property/value pair, with its important flag.
///
/// # Custom properties share this type, deliberately
///
/// A declaration whose property starts with `--` (`--ink: #0a0a0a`) is a
/// [custom property](https://drafts.csswg.org/css-variables/), not a
/// standard one, and it is stored in this same struct rather than a parallel
/// type. That is a narrower change than it looks: this syntax layer already
/// stores every value as unparsed text and validates none of them at parse
/// time — colour, length, and every other per-property grammar is checked
/// only when a consumer asks a property implementation (such as
/// [`Color::parse`]) to interpret the resolved string. A custom property's
/// value needs exactly that treatment: opaque text, substituted verbatim
/// wherever a `var()` reference names it. The one place custom properties do
/// need different handling is `property` itself: standard property names are
/// ASCII case-insensitive and are lowercased here, but a custom property's
/// name is case-sensitive (`--Ink` and `--ink` are different properties), so
/// the declaration-block parser preserves its case rather than folding it.
///
/// What genuinely differs is handled outside this struct: custom properties
/// inherit unconditionally (unlike most standard properties, which inherit
/// selectively or not at all), which is why resolving a `var()` reference
/// needs to walk ancestors — see [`resolve_declarations`] — rather than
/// something this crate's plain per-element `cascade` could express.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Declaration {
    /// Property name. Lowercased for a standard property; case-preserved for
    /// a custom property (one starting with `--`).
    pub property: String,
    /// Value text, unparsed. Value parsing is per-property and belongs to the
    /// property implementations, not the syntax layer.
    pub value: String,
    /// Whether `!important` was present.
    pub important: bool,
}

/// Returns whether `property` names a custom property rather than a
/// standard one.
///
/// A custom property is any property whose name begins with two dashes,
/// per the CSS Custom Properties specification. This is the one bit of
/// vocabulary the cascade and `var()` machinery need to share, so it is a
/// named function rather than a `starts_with("--")` repeated at each call
/// site.
#[must_use]
pub fn is_custom_property(property: &str) -> bool {
    property.starts_with("--")
}

/// A style rule: a selector list and a declaration block.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Rule {
    /// Selectors that share this block.
    pub selectors: Vec<Selector>,
    /// Declarations in source order.
    pub declarations: Vec<Declaration>,
}

/// A parsed stylesheet.
#[derive(Clone, Debug, Default, Eq, PartialEq)]
pub struct Stylesheet {
    /// Rules in source order. Order is part of the cascade.
    pub rules: Vec<Rule>,
}

impl Stylesheet {
    /// Parses `source` into a stylesheet.
    ///
    /// # Errors
    ///
    /// Returns [`CssError`] for constructs this implementation does not model,
    /// rather than dropping them and matching the wrong elements.
    pub fn parse(source: &str) -> Result<Self, CssError> {
        Parser::new(source).parse_stylesheet()
    }
}

// -- parsing -------------------------------------------------------------

struct Parser<'source> {
    bytes: &'source [u8],
    position: usize,
}

impl<'source> Parser<'source> {
    const fn new(source: &'source str) -> Self {
        Self {
            bytes: source.as_bytes(),
            position: 0,
        }
    }

    fn parse_stylesheet(&mut self) -> Result<Stylesheet, CssError> {
        let mut rules = Vec::new();
        loop {
            self.skip_trivia();
            if self.position >= self.bytes.len() {
                break;
            }
            if self.bytes[self.position] == b'@' {
                let name = self.read_at_rule_name();
                return Err(CssError::AtRuleUnsupported { name });
            }
            rules.push(self.parse_rule()?);
        }
        Ok(Stylesheet { rules })
    }

    fn parse_rule(&mut self) -> Result<Rule, CssError> {
        let prelude_start = self.position;
        while self.position < self.bytes.len() && self.bytes[self.position] != b'{' {
            self.position += 1;
        }
        if self.position >= self.bytes.len() {
            return Err(CssError::UnterminatedBlock {
                offset: prelude_start,
            });
        }
        let prelude = self.slice(prelude_start, self.position);
        self.position += 1; // consume '{'

        let block_start = self.position;
        while self.position < self.bytes.len() && self.bytes[self.position] != b'}' {
            self.position += 1;
        }
        if self.position >= self.bytes.len() {
            return Err(CssError::UnterminatedBlock {
                offset: block_start,
            });
        }
        let block = self.slice(block_start, self.position);
        self.position += 1; // consume '}'

        Ok(Rule {
            selectors: parse_selector_list(&prelude)?,
            declarations: parse_declarations(&block),
        })
    }

    fn read_at_rule_name(&mut self) -> String {
        let start = self.position + 1;
        let mut end = start;
        while end < self.bytes.len()
            && (self.bytes[end].is_ascii_alphanumeric() || self.bytes[end] == b'-')
        {
            end += 1;
        }
        self.position = end;
        self.slice(start, end)
    }

    fn slice(&self, start: usize, end: usize) -> String {
        core::str::from_utf8(&self.bytes[start..end])
            .unwrap_or_default()
            .to_string()
    }

    fn skip_trivia(&mut self) {
        loop {
            while self.position < self.bytes.len()
                && self.bytes[self.position].is_ascii_whitespace()
            {
                self.position += 1;
            }
            if self.bytes[self.position..].starts_with(b"/*") {
                self.position += 2;
                while self.position < self.bytes.len()
                    && !self.bytes[self.position..].starts_with(b"*/")
                {
                    self.position += 1;
                }
                self.position = (self.position + 2).min(self.bytes.len());
                continue;
            }
            break;
        }
    }
}

fn parse_selector_list(prelude: &str) -> Result<Vec<Selector>, CssError> {
    let mut selectors = Vec::new();
    for piece in prelude.split(',') {
        let text = piece.trim();
        if text.is_empty() {
            continue;
        }
        selectors.push(parse_selector(text)?);
    }
    if selectors.is_empty() {
        return Err(CssError::MalformedSelector {
            text: prelude.trim().to_string(),
        });
    }
    Ok(selectors)
}

fn parse_selector(text: &str) -> Result<Selector, CssError> {
    // Split into compounds and combinators. Whitespace is a descendant
    // combinator unless an explicit combinator character is present.
    let mut compounds: Vec<Compound> = Vec::new();
    let mut combinators: Vec<Combinator> = Vec::new();
    let mut current = String::new();
    let mut pending: Option<Combinator> = None;
    let mut saw_space = false;

    for character in text.chars() {
        match character {
            '>' | '+' | '~' => {
                if !current.trim().is_empty() {
                    compounds.push(parse_compound(current.trim())?);
                    if let Some(combinator) = pending.take() {
                        combinators.push(combinator);
                    }
                    current.clear();
                }
                pending = Some(match character {
                    '>' => Combinator::Child,
                    '+' => Combinator::NextSibling,
                    _ => Combinator::SubsequentSibling,
                });
                saw_space = false;
            }
            c if c.is_whitespace() => {
                if !current.trim().is_empty() {
                    saw_space = true;
                }
            }
            _ => {
                if saw_space && !current.trim().is_empty() {
                    compounds.push(parse_compound(current.trim())?);
                    combinators.push(pending.take().unwrap_or(Combinator::Descendant));
                    current.clear();
                }
                saw_space = false;
                current.push(character);
            }
        }
    }
    if !current.trim().is_empty() {
        compounds.push(parse_compound(current.trim())?);
        if let Some(combinator) = pending.take() {
            combinators.push(combinator);
        }
    }
    if compounds.is_empty() {
        return Err(CssError::MalformedSelector {
            text: text.to_string(),
        });
    }

    // The rightmost compound is the subject; the rest are constraints listed
    // nearest-first, which is the order matching walks them.
    let subject = compounds.pop().unwrap_or_default();
    let mut ancestors = Vec::new();
    while let Some(compound) = compounds.pop() {
        let combinator = combinators.pop().unwrap_or(Combinator::Descendant);
        ancestors.push((combinator, compound));
    }
    Ok(Selector { subject, ancestors })
}

fn parse_compound(text: &str) -> Result<Compound, CssError> {
    let mut parts = Vec::new();
    let bytes = text.as_bytes();
    let mut index = 0;

    while index < bytes.len() {
        match bytes[index] {
            b'*' => {
                parts.push(SimpleSelector::Universal);
                index += 1;
            }
            b'.' => {
                let (name, next) = read_ident(bytes, index + 1);
                if name.is_empty() {
                    return Err(CssError::MalformedSelector {
                        text: text.to_string(),
                    });
                }
                parts.push(SimpleSelector::Class(name));
                index = next;
            }
            b'#' => {
                let (name, next) = read_ident(bytes, index + 1);
                if name.is_empty() {
                    return Err(CssError::MalformedSelector {
                        text: text.to_string(),
                    });
                }
                parts.push(SimpleSelector::Id(name));
                index = next;
            }
            b'[' => {
                let close = text[index..]
                    .find(']')
                    .ok_or_else(|| CssError::MalformedSelector {
                        text: text.to_string(),
                    })?
                    + index;
                let inner = &text[index + 1..close];
                parts.push(parse_attribute_selector(inner, text)?);
                index = close + 1;
            }
            b':' => {
                // `::x` is a pseudo-element; `:x` is a pseudo-class. Both change
                // matching, so every one but `:hover` is refused rather than
                // dropped.
                let double = bytes.get(index + 1) == Some(&b':');
                let start = if double { index + 2 } else { index + 1 };
                let (name, next) = read_ident(bytes, start);
                if !double && name == "hover" {
                    parts.push(SimpleSelector::Hover);
                    index = next;
                    continue;
                }
                return Err(if double {
                    CssError::PseudoElementUnsupported { name }
                } else {
                    CssError::PseudoClassUnsupported { name }
                });
            }
            _ => {
                let (name, next) = read_ident(bytes, index);
                if name.is_empty() {
                    return Err(CssError::MalformedSelector {
                        text: text.to_string(),
                    });
                }
                parts.push(SimpleSelector::Type(name.to_ascii_lowercase()));
                index = next;
            }
        }
    }

    if parts.is_empty() {
        return Err(CssError::MalformedSelector {
            text: text.to_string(),
        });
    }
    Ok(Compound { parts })
}

fn parse_attribute_selector(inner: &str, whole: &str) -> Result<SimpleSelector, CssError> {
    if let Some((name, value)) = inner.split_once('=') {
        let value = value.trim().trim_matches(['"', '\'']).to_string();
        let name = name.trim();
        // Only exact equality is modeled. Operators such as ^=, |=, and *=
        // change which elements match, so they are refused.
        if name.ends_with(['^', '$', '*', '~', '|']) {
            return Err(CssError::MalformedSelector {
                text: whole.to_string(),
            });
        }
        Ok(SimpleSelector::AttributeEquals {
            name: name.to_ascii_lowercase(),
            value,
        })
    } else {
        Ok(SimpleSelector::AttributePresent(
            inner.trim().to_ascii_lowercase(),
        ))
    }
}

fn read_ident(bytes: &[u8], start: usize) -> (String, usize) {
    let mut end = start;
    while end < bytes.len()
        && (bytes[end].is_ascii_alphanumeric() || bytes[end] == b'-' || bytes[end] == b'_')
    {
        end += 1;
    }
    (
        core::str::from_utf8(&bytes[start..end])
            .unwrap_or_default()
            .to_string(),
        end,
    )
}

fn parse_declarations(block: &str) -> Vec<Declaration> {
    let mut declarations = Vec::new();
    for piece in block.split(';') {
        let text = piece.trim();
        if text.is_empty() {
            continue;
        }
        let Some((property, value)) = text.split_once(':') else {
            // A declaration without a colon is dropped, which is what the
            // specification's error handling requires.
            continue;
        };
        let raw_property = property.trim();
        // Standard property names are ASCII case-insensitive, so `COLOR` and
        // `color` must collide; a custom property's name is case-sensitive,
        // so `--Ink` and `--ink` must not. Folding both the same way would
        // make one of those two rules wrong.
        let property = if is_custom_property(raw_property) {
            raw_property.to_string()
        } else {
            raw_property.to_ascii_lowercase()
        };
        let mut value = value.trim().to_string();
        let important = value.to_ascii_lowercase().ends_with("!important");
        if important {
            let cut = value.len() - "!important".len();
            value = value[..cut].trim().to_string();
        }
        if property.is_empty() || value.is_empty() {
            continue;
        }
        declarations.push(Declaration {
            property,
            value,
            important,
        });
    }
    declarations
}

// -- matching ------------------------------------------------------------

/// Returns whether `selector` matches `element` in `tree`.
///
/// `hovered` names the one element currently under the pointer, if any — the
/// only fact `:hover` needs. `None` means nothing is hovered, so no `:hover`
/// condition anywhere in the selector can be satisfied.
#[must_use]
pub fn matches<T: ElementTree>(
    tree: &T,
    element: T::Node,
    selector: &Selector,
    hovered: Option<T::Node>,
) -> bool {
    if !compound_matches(tree, element, &selector.subject, hovered) {
        return false;
    }
    let mut current = element;
    for (combinator, compound) in &selector.ancestors {
        match combinator {
            Combinator::Descendant => match find_ancestor(tree, current, compound, hovered) {
                Some(found) => current = found,
                None => return false,
            },
            Combinator::Child => {
                let Some(parent) = tree.parent(current) else {
                    return false;
                };
                if !compound_matches(tree, parent, compound, hovered) {
                    return false;
                }
                current = parent;
            }
            Combinator::NextSibling => {
                let Some(previous) = tree.previous_element_sibling(current) else {
                    return false;
                };
                if !compound_matches(tree, previous, compound, hovered) {
                    return false;
                }
                current = previous;
            }
            Combinator::SubsequentSibling => {
                let mut cursor = tree.previous_element_sibling(current);
                let mut found = None;
                while let Some(candidate) = cursor {
                    if compound_matches(tree, candidate, compound, hovered) {
                        found = Some(candidate);
                        break;
                    }
                    cursor = tree.previous_element_sibling(candidate);
                }
                match found {
                    Some(node) => current = node,
                    None => return false,
                }
            }
        }
    }
    true
}

fn find_ancestor<T: ElementTree>(
    tree: &T,
    from: T::Node,
    compound: &Compound,
    hovered: Option<T::Node>,
) -> Option<T::Node> {
    let mut cursor = tree.parent(from);
    while let Some(candidate) = cursor {
        if compound_matches(tree, candidate, compound, hovered) {
            return Some(candidate);
        }
        cursor = tree.parent(candidate);
    }
    None
}

fn compound_matches<T: ElementTree>(
    tree: &T,
    element: T::Node,
    compound: &Compound,
    hovered: Option<T::Node>,
) -> bool {
    if !tree.is_element(element) {
        return false;
    }
    compound.parts.iter().all(|part| match part {
        SimpleSelector::Universal => true,
        SimpleSelector::Type(expected) => tree.tag_name(element) == Some(expected.as_str()),
        // A class attribute is a whitespace-separated list, so a substring
        // test here would leak styles onto unrelated elements.
        SimpleSelector::Class(expected) => tree
            .attribute(element, "class")
            .is_some_and(|value| value.split_whitespace().any(|c| c == expected)),
        SimpleSelector::Id(expected) => tree.attribute(element, "id") == Some(expected.as_str()),
        SimpleSelector::AttributePresent(expected) => tree.attribute(element, expected).is_some(),
        SimpleSelector::AttributeEquals { name: key, value } => {
            tree.attribute(element, key) == Some(value.as_str())
        }
        SimpleSelector::Hover => hovered == Some(element),
    })
}

// -- cascade -------------------------------------------------------------

/// A declaration that won the cascade for one property.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ComputedDeclaration {
    /// The winning value.
    pub value: String,
    /// Whether the winner was marked important.
    pub important: bool,
    /// Specificity of the selector that supplied it.
    pub specificity: Specificity,
    /// Index of the rule in source order, used to break specificity ties.
    pub source_order: usize,
}

/// Resolves which declarations apply to `element`.
///
/// Ordering follows the cascade: important declarations outrank normal ones,
/// then higher specificity wins, then later source order wins. Inline styles
/// and user-agent or user origins are not modeled here; this resolves author
/// stylesheet rules only.
#[must_use]
/// The key a rule is filed under, taken from its subject compound.
///
/// Most selectors name something specific about the element they end on, so
/// most rules can be skipped without being evaluated at all.
#[derive(Clone, Debug, Eq, Hash, PartialEq)]
enum Key {
    Id(String),
    Class(String),
    Type(String),
}

/// Rules grouped by what their rightmost compound requires.
///
/// # Why this exists
///
/// Matching every rule against every element is quadratic in document size,
/// and measurably so: 200 rules over 200 elements took 1.4 ms, while 1600 over
/// 1600 took 95 ms — eight times the input for sixty-seven times the work.
/// Correct the whole way, and unusable on a real page.
///
/// # What it does not help
///
/// Selectivity, not rule count. A stylesheet of `div` rules against a document
/// of `div` elements still evaluates every pair, because every pair genuinely
/// matches. The index removes work that was never going to match; it cannot
/// remove work that was.
#[derive(Debug, Default)]
pub struct SelectorIndex {
    buckets: std::collections::HashMap<Key, Vec<usize>>,
    /// Rules whose subject names nothing indexable — `*`, or an attribute
    /// condition alone. Evaluated for every element, because skipping them
    /// would silently drop matches.
    unkeyed: Vec<usize>,
    rules: Vec<Rule>,
}

impl SelectorIndex {
    /// Builds an index over `stylesheet`.
    #[must_use]
    pub fn build(stylesheet: &Stylesheet) -> Self {
        let mut index = Self {
            rules: stylesheet.rules.clone(),
            ..Self::default()
        };
        for (order, rule) in stylesheet.rules.iter().enumerate() {
            // Every selector in a list is filed separately, all pointing at the
            // same rule. Filing `div, .foo` under one key only would silently
            // stop the other selector from ever matching.
            for selector in &rule.selectors {
                match subject_key(&selector.subject) {
                    Some(key) => index.buckets.entry(key).or_default().push(order),
                    None => index.unkeyed.push(order),
                }
            }
        }
        index
    }

    /// Returns how many rules would be evaluated for `element`.
    ///
    /// A diagnostic, and the basis of the regression test for this index: the
    /// mechanism is "consider fewer rules", and asserting that directly is
    /// deterministic where asserting elapsed time is not. A wall-clock check in
    /// a test suite is a flaky failure waiting for a loaded machine.
    #[must_use]
    pub fn candidate_count<T: ElementTree>(&self, tree: &T, element: T::Node) -> usize {
        self.candidates(tree, element).len()
    }

    /// Returns the total number of rules in the stylesheet.
    #[must_use]
    pub fn rule_count(&self) -> usize {
        self.rules.len()
    }

    /// Returns the rule indices that could match `element`, in source order.
    fn candidates<T: ElementTree>(&self, tree: &T, element: T::Node) -> Vec<usize> {
        let mut candidates = self.unkeyed.clone();

        if let Some(id) = tree.attribute(element, "id")
            && let Some(bucket) = self.buckets.get(&Key::Id(id.to_string()))
        {
            candidates.extend(bucket);
        }
        if let Some(classes) = tree.attribute(element, "class") {
            for class in classes.split_whitespace() {
                if let Some(bucket) = self.buckets.get(&Key::Class(class.to_string())) {
                    candidates.extend(bucket);
                }
            }
        }
        if let Some(tag) = tree.tag_name(element)
            && let Some(bucket) = self.buckets.get(&Key::Type(tag.to_string()))
        {
            candidates.extend(bucket);
        }

        // A rule reached through several selectors appears more than once.
        // Evaluating it twice would be wasteful rather than wrong; sorting also
        // restores source order, which keeps iteration deterministic.
        candidates.sort_unstable();
        candidates.dedup();
        candidates
    }
}

/// Returns the key a compound is filed under.
///
/// Id beats class beats type, which is the order of how much each narrows the
/// candidate set. `*`, and compounds carrying only attribute conditions, have
/// no key and go to the unkeyed list rather than being dropped.
fn subject_key(compound: &Compound) -> Option<Key> {
    let mut class = None;
    let mut tag = None;
    for part in &compound.parts {
        match part {
            SimpleSelector::Id(name) => return Some(Key::Id(name.clone())),
            SimpleSelector::Class(name) if class.is_none() => class = Some(name.clone()),
            SimpleSelector::Type(name) if tag.is_none() => tag = Some(name.clone()),
            _ => {}
        }
    }
    class.map(Key::Class).or_else(|| tag.map(Key::Type))
}

/// Resolves the declarations that apply to `element`, considering only the
/// rules the index says could match.
///
/// Equivalent to [`cascade_reference`] by construction and by test. Every
/// candidate carries its `source_order` explicitly rather than inheriting it
/// from iteration, so visiting rules in bucket order cannot change which
/// declaration wins — the failure this optimisation would otherwise invite.
///
/// `hovered` is forwarded to [`matches`] for every candidate rule; pass
/// `None` when nothing is under the pointer.
#[must_use]
pub fn cascade<T: ElementTree>(
    tree: &T,
    element: T::Node,
    index: &SelectorIndex,
    hovered: Option<T::Node>,
) -> Vec<(String, ComputedDeclaration)> {
    let mut winners: Vec<(String, ComputedDeclaration)> = Vec::new();

    for order in index.candidates(tree, element) {
        let rule = &index.rules[order];
        let Some(specificity) = rule
            .selectors
            .iter()
            .filter(|selector| matches(tree, element, selector, hovered))
            .map(Selector::specificity)
            .max()
        else {
            continue;
        };
        accumulate(&mut winners, rule, specificity, order);
    }

    winners.sort_by(|left, right| left.0.cmp(&right.0));
    winners
}

/// Folds one matching rule's declarations into the winning set.
///
/// Shared by both cascades so they cannot drift in how a tie is resolved.
fn accumulate(
    winners: &mut Vec<(String, ComputedDeclaration)>,
    rule: &Rule,
    specificity: Specificity,
    order: usize,
) {
    for declaration in &rule.declarations {
        let candidate = ComputedDeclaration {
            value: declaration.value.clone(),
            important: declaration.important,
            specificity,
            source_order: order,
        };
        match winners
            .iter_mut()
            .find(|(property, _)| *property == declaration.property)
        {
            Some((_, existing)) => {
                if beats(&candidate, existing) {
                    *existing = candidate;
                }
            }
            None => winners.push((declaration.property.clone(), candidate)),
        }
    }
}

/// The unindexed cascade, kept as the reference the indexed one is checked
/// against.
///
/// Public so a differential test in another crate can reach it. Not for
/// production use: it evaluates every rule against every element, which is the
/// quadratic behaviour [`SelectorIndex`] exists to remove. It stays because an
/// optimisation with nothing to compare against is an assertion rather than a
/// result.
#[must_use]
pub fn cascade_reference<T: ElementTree>(
    tree: &T,
    element: T::Node,
    stylesheet: &Stylesheet,
    hovered: Option<T::Node>,
) -> Vec<(String, ComputedDeclaration)> {
    let mut winners: Vec<(String, ComputedDeclaration)> = Vec::new();

    for (order, rule) in stylesheet.rules.iter().enumerate() {
        let Some(specificity) = rule
            .selectors
            .iter()
            .filter(|selector| matches(tree, element, selector, hovered))
            .map(Selector::specificity)
            .max()
        else {
            continue;
        };
        accumulate(&mut winners, rule, specificity, order);
    }

    winners.sort_by(|left, right| left.0.cmp(&right.0));
    winners
}

/// Returns whether `candidate` outranks `existing` under the cascade order.
fn beats(candidate: &ComputedDeclaration, existing: &ComputedDeclaration) -> bool {
    match (candidate.important, existing.important) {
        (true, false) => true,
        (false, true) => false,
        _ => match candidate.specificity.cmp(&existing.specificity) {
            core::cmp::Ordering::Greater => true,
            core::cmp::Ordering::Less => false,
            // Equal specificity: later source order wins.
            core::cmp::Ordering::Equal => candidate.source_order >= existing.source_order,
        },
    }
}

// -- custom properties -----------------------------------------------------

/// How many `var()` calls a fallback, or a chain of custom properties that
/// reference one another, may nest before resolution is refused.
///
/// # Why a limit exists
///
/// A custom property's value can itself contain `var()` — `--gap: var(--space)`
/// — and a `var()` fallback can contain another `var()` call —
/// `var(--a, var(--b, red))`. Both are resolved by recursing, and both are
/// driven by stylesheet text this crate does not control: a page (or, per
/// `AGENTS.md`'s rule to bound recursion on untrusted input, a hostile one)
/// can nest either arbitrarily deep, and a custom property can even name
/// itself (`--a: var(--a)`) to build a cycle with no natural base case. A
/// depth counter turns both the ordinary case and the adversarial one into
/// the same bounded check: real design-token chains are a handful of levels
/// deep, so thirty-two is generous headroom, and a chain that reaches it is
/// refused with [`CssError::CustomPropertyNestingTooDeep`] rather than
/// recursing until the stack gives out.
const MAX_VAR_NESTING: u32 = 32;

/// Resolves every `var(--name)` and `var(--name, fallback)` reference in
/// `value` against `environment`, returning the value with all of them
/// substituted.
///
/// `environment` maps a custom property name to its own cascaded value,
/// *unresolved* — see [`custom_property_environment`] for why substitution is
/// deferred to here rather than done while building it.
///
/// # Supported nesting
///
/// A referenced custom property's value may itself contain `var()`
/// references (resolved against the same environment), and a fallback may
/// itself be, or contain, a `var()` call. Both recurse through this
/// function, sharing one depth counter bounded by [`MAX_VAR_NESTING`] — see
/// its doc comment for why cycles and pathological nesting are refused
/// rather than parsed wrong.
fn resolve_var_references(
    value: &str,
    environment: &std::collections::HashMap<String, String>,
) -> Result<String, CssError> {
    resolve_var_references_at_depth(value, environment, 0)
}

fn resolve_var_references_at_depth(
    value: &str,
    environment: &std::collections::HashMap<String, String>,
    depth: u32,
) -> Result<String, CssError> {
    let characters: Vec<char> = value.chars().collect();
    let mut result = String::new();
    let mut index = 0;
    while index < characters.len() {
        if is_var_call_at(&characters, index) {
            let open_paren = index + 3;
            let close_paren = find_matching_paren(&characters, open_paren).ok_or_else(|| {
                CssError::CustomPropertySyntax {
                    text: value.to_string(),
                }
            })?;
            let inner: String = characters[open_paren + 1..close_paren].iter().collect();
            let substitution = resolve_var_call(&inner, environment, depth, value)?;
            result.push_str(&substitution);
            index = close_paren + 1;
        } else {
            result.push(characters[index]);
            index += 1;
        }
    }
    Ok(result)
}

/// Returns whether a `var(` function call starts at `index`.
///
/// A preceding identifier character (letter, digit, `-`, or `_`) means this
/// is the tail of some other name — `--somevar(` is one identifier token,
/// not the custom property `--some` followed by a call — so that case is
/// excluded rather than misread as `var()`.
fn is_var_call_at(characters: &[char], index: usize) -> bool {
    if index + 4 > characters.len() {
        return false;
    }
    if characters[index] != 'v'
        || characters[index + 1] != 'a'
        || characters[index + 2] != 'r'
        || characters[index + 3] != '('
    {
        return false;
    }
    match index.checked_sub(1).and_then(|i| characters.get(i)) {
        Some(previous) => {
            !(previous.is_ascii_alphanumeric() || *previous == '-' || *previous == '_')
        }
        None => true,
    }
}

/// Returns the index of the `)` matching the `(` at `open_index`, accounting
/// for parentheses nested inside (a fallback may itself contain a function
/// call, `var()` or otherwise).
fn find_matching_paren(characters: &[char], open_index: usize) -> Option<usize> {
    let mut depth: i32 = 0;
    for (offset, character) in characters[open_index..].iter().enumerate() {
        match character {
            '(' => depth += 1,
            ')' => {
                depth -= 1;
                if depth == 0 {
                    return Some(open_index + offset);
                }
            }
            _ => {}
        }
    }
    None
}

/// Splits `characters` at its first top-level comma (one not nested inside
/// parentheses), returning the name argument and, if a comma was found, the
/// remaining text as the fallback.
///
/// Only the first comma is a delimiter: CSS fallback values routinely
/// contain their own commas (`var(--font, Arial, sans-serif)`), and the
/// fallback there is `Arial, sans-serif` whole, not `Arial` alone.
fn split_top_level_comma(characters: &[char]) -> (String, Option<String>) {
    let mut depth: i32 = 0;
    for (position, character) in characters.iter().enumerate() {
        match character {
            '(' => depth += 1,
            ')' => depth -= 1,
            ',' if depth == 0 => {
                let name: String = characters[..position].iter().collect();
                let fallback: String = characters[position + 1..].iter().collect();
                return (name, Some(fallback));
            }
            _ => {}
        }
    }
    (characters.iter().collect(), None)
}

/// Resolves one `var(...)` call's arguments (`inner`, the text between its
/// parentheses) to a substitution string.
fn resolve_var_call(
    inner: &str,
    environment: &std::collections::HashMap<String, String>,
    depth: u32,
    whole_value: &str,
) -> Result<String, CssError> {
    if depth >= MAX_VAR_NESTING {
        return Err(CssError::CustomPropertyNestingTooDeep {
            text: whole_value.to_string(),
        });
    }
    let characters: Vec<char> = inner.chars().collect();
    let (name_part, fallback_part) = split_top_level_comma(&characters);
    let name = name_part.trim();
    // A var() reference must name a custom property: `var()` with nothing in
    // it, or `var(--, ...)` with nothing after the two dashes, both fail
    // this, and so does `var(color)`, which does not start with `--` at all.
    if !is_custom_property(name) || name.len() <= 2 {
        return Err(CssError::CustomPropertySyntax {
            text: whole_value.to_string(),
        });
    }

    if let Some(raw) = environment.get(name) {
        // The referenced custom property's own value may reference further
        // custom properties (`--gap: var(--space)`); resolving it here,
        // lazily, rather than when the environment was built, means a
        // custom property nobody actually uses can be malformed or
        // undefined without refusing every element that merely inherits it.
        return resolve_var_references_at_depth(raw, environment, depth + 1);
    }

    match fallback_part {
        Some(fallback) => resolve_var_references_at_depth(fallback.trim(), environment, depth + 1),
        None => Err(CssError::CustomPropertyUndefined {
            name: name.to_string(),
        }),
    }
}

/// Returns `element` and its ancestors, root first.
///
/// Root-first order is what lets [`custom_property_environment`] express
/// inheritance as a fold: a descendant's own declaration simply overwrites
/// whatever an ancestor contributed for the same name, which is exactly how
/// a nearer declaration is supposed to beat an inherited one.
fn ancestor_chain<T: ElementTree>(tree: &T, element: T::Node) -> Vec<T::Node> {
    let mut chain = vec![element];
    let mut current = element;
    while let Some(parent) = tree.parent(current) {
        chain.push(parent);
        current = parent;
    }
    chain.reverse();
    chain
}

/// Builds the custom-property environment visible at `element`: for every
/// custom property declared anywhere from the document root down to
/// `element` inclusive, the value that wins the cascade at the nearest node
/// that declares it.
///
/// # Why this exists, when [`cascade`] already resolves one element
///
/// `cascade` (deliberately, per this crate's scope) does not inherit: it
/// reports only the declarations whose selectors match the element passed
/// to it. Custom properties inherit unconditionally, so a `var()` reference
/// three levels below the rule that declared the custom property has to see
/// it anyway. This function is the walk that makes that true: it calls
/// `cascade` once per ancestor — cheap, because a document's depth is
/// nowhere near its element count — and keeps only the properties whose
/// name starts with `--`, letting a closer declaration shadow a farther one
/// simply by being inserted later.
///
/// # Why values here are not yet `var()`-resolved
///
/// Resolving every custom property's value while building this map would
/// mean one broken definition — an undefined reference, a cycle — poisons
/// the whole environment, refusing elements that never touch that property.
/// [`resolve_var_references`] resolves a stored value lazily, only when
/// something actually asks for it, which is the same reasoning `cascade`
/// itself already applies to per-property value validation: an error should
/// be attributable to the thing that actually needed the missing value.
fn custom_property_environment<T: ElementTree>(
    tree: &T,
    chain: &[T::Node],
    index: &SelectorIndex,
    hovered: Option<T::Node>,
) -> std::collections::HashMap<String, String> {
    let mut environment = std::collections::HashMap::new();
    for &node in chain {
        for (property, computed) in cascade(tree, node, index, hovered) {
            if is_custom_property(&property) {
                environment.insert(property, computed.value);
            }
        }
    }
    environment
}

/// Resolves the declarations that apply to `element`, with every `var()`
/// reference in a standard property's value substituted for the custom
/// property it names — following the same cascade, specificity, and
/// inheritance rules as any other property, per the CSS Custom Properties
/// specification.
///
/// Declarations for the custom properties themselves (property names
/// starting with `--`) are returned unresolved, verbatim: `var()`
/// substitution is scoped to standard properties that *use* a custom
/// property, not to the custom property's own stored text, matching this
/// crate's wider policy of leaving a value unparsed until something asks to
/// interpret it. Also see this module's custom-property environment builder
/// for why a broken custom property does not refuse elements that never
/// reference it.
///
/// # Errors
///
/// Returns [`CssError::CustomPropertyUndefined`] if a standard property's
/// value names a custom property that is not declared anywhere from the
/// document root down to `element`, and gives no fallback;
/// [`CssError::CustomPropertySyntax`] for a `var()` call this
/// implementation cannot parse (no arguments, unmatched parentheses, or a
/// name not starting with `--`); and
/// [`CssError::CustomPropertyNestingTooDeep`] for fallback or custom-property
/// chains nested past the bound documented on `MAX_VAR_NESTING`.
pub fn resolve_declarations<T: ElementTree>(
    tree: &T,
    element: T::Node,
    index: &SelectorIndex,
    hovered: Option<T::Node>,
) -> Result<Vec<(String, ComputedDeclaration)>, CssError> {
    let chain = ancestor_chain(tree, element);
    let environment = custom_property_environment(tree, &chain, index, hovered);
    let winners = cascade(tree, element, index, hovered);

    let mut resolved = Vec::with_capacity(winners.len());
    for (property, computed) in winners {
        if is_custom_property(&property) {
            resolved.push((property, computed));
            continue;
        }
        let value = resolve_var_references(&computed.value, &environment)?;
        resolved.push((property, ComputedDeclaration { value, ..computed }));
    }
    Ok(resolved)
}

// -- turing-html adapter -------------------------------------------------

/// Implements [`ElementTree`] for the engine's own document.
///
/// Behind the `html` feature so the core selector engine carries no
/// dependency. This is the reference implementation of the trait, and it is
/// also the shape an embedder copies for their own tree.
#[cfg(feature = "html")]
mod html_tree {
    use super::ElementTree;
    use turing_html::{Document, NodeData, NodeId};

    impl ElementTree for Document {
        type Node = NodeId;

        fn is_element(&self, node: Self::Node) -> bool {
            matches!(self.node(node).data, NodeData::Element { .. })
        }

        fn tag_name(&self, node: Self::Node) -> Option<&str> {
            self.element_name(node)
        }

        fn attribute(&self, node: Self::Node, name: &str) -> Option<&str> {
            let NodeData::Element { attributes, .. } = &self.node(node).data else {
                return None;
            };
            attributes
                .iter()
                .find(|attribute| attribute.name == name)
                .map(|attribute| attribute.value.as_str())
        }

        fn parent(&self, node: Self::Node) -> Option<Self::Node> {
            self.node(node).parent
        }

        fn previous_element_sibling(&self, node: Self::Node) -> Option<Self::Node> {
            let parent = self.node(node).parent?;
            let siblings = &self.node(parent).children;
            let index = siblings.iter().position(|&id| id == node)?;
            siblings[..index]
                .iter()
                .rev()
                .copied()
                .find(|&id| self.is_element(id))
        }
    }
}

#[cfg(all(test, feature = "html"))]
mod tests {
    use super::*;
    use turing_html::{Document, NodeId, Tokenizer, TreeBuilder};

    fn document(html: &str) -> Document {
        let tokens = Tokenizer::new(html).tokenize().expect("tokenizes").tokens;
        TreeBuilder::new().build(&tokens).expect("builds")
    }

    fn find(document: &Document, name: &str) -> NodeId {
        (0..document.len())
            .map(NodeId::from_index)
            .find(|&id| document.element_name(id) == Some(name))
            .expect("element exists")
    }

    fn declarations(html: &str, css: &str, element: &str) -> Vec<(String, String)> {
        let doc = document(html);
        let sheet = Stylesheet::parse(css).expect("parses");
        let node = find(&doc, element);

        // Every cascade test below is also a differential test: the indexed and
        // reference paths must agree, or the index has changed a result rather
        // than only skipping work that could not have matched.
        let indexed = cascade(&doc, node, &SelectorIndex::build(&sheet), None);
        let reference = cascade_reference(&doc, node, &sheet, None);
        assert_eq!(
            indexed, reference,
            "selector index disagreed with the reference cascade"
        );

        indexed
            .into_iter()
            .map(|(property, computed)| (property, computed.value))
            .collect()
    }

    /// Like [`declarations`], but resolving `var()` references — the entry
    /// point the custom-property tests below exercise.
    fn resolved_declarations(
        html: &str,
        css: &str,
        element: &str,
    ) -> Result<Vec<(String, String)>, CssError> {
        let doc = document(html);
        let sheet = Stylesheet::parse(css).expect("parses");
        let node = find(&doc, element);
        let index = SelectorIndex::build(&sheet);
        let resolved = resolve_declarations(&doc, node, &index, None)?;
        Ok(resolved
            .into_iter()
            .map(|(property, computed)| (property, computed.value))
            .collect())
    }

    #[test]
    fn the_named_set_is_the_complete_css_color_4_table() {
        // Spot checks across the alphabet, including the newest name and the
        // shared-value aliases.
        for (name, expected) in [
            ("aliceblue", (0xf0, 0xf8, 0xff)),
            ("cornflowerblue", (0x64, 0x95, 0xed)),
            ("rebeccapurple", (0x66, 0x33, 0x99)),
            ("yellowgreen", (0x9a, 0xcd, 0x32)),
            ("cyan", (0x00, 0xff, 0xff)),
            ("aqua", (0x00, 0xff, 0xff)),
            ("magenta", (0xff, 0x00, 0xff)),
            ("darkslategrey", (0x2f, 0x4f, 0x4f)),
        ] {
            let color = Color::parse(name).expect(name);
            assert_eq!((color.red, color.green, color.blue), expected, "{name}");
        }
    }

    #[test]
    fn rgb_notation_parses_in_its_common_forms() {
        for (value, expected) in [
            ("rgb(255, 0, 0)", (255, 0, 0)),
            ("rgb(0 128 255)", (0, 128, 255)),
            ("rgb(50%, 0%, 100%)", (128, 0, 255)),
            ("rgba(10, 20, 30, 1)", (10, 20, 30)),
            ("rgb(0 128 255 / 1)", (0, 128, 255)),
            // Out-of-range channels clamp, per the specification.
            ("rgb(300, -5, 42)", (255, 0, 42)),
        ] {
            let color = Color::parse(value).expect(value);
            assert_eq!((color.red, color.green, color.blue), expected, "{value}");
        }
    }

    #[test]
    fn hsl_notation_matches_the_specification_conversion() {
        for (value, expected) in [
            ("hsl(0, 100%, 50%)", (255, 0, 0)),
            ("hsl(120, 100%, 25%)", (0, 128, 0)),
            ("hsl(240 100% 50%)", (0, 0, 255)),
            ("hsl(0, 0%, 50%)", (128, 128, 128)),
            ("hsla(300, 100%, 50%, 1)", (255, 0, 255)),
            ("hsl(480deg, 100%, 50%)", (0, 255, 0)),
        ] {
            let color = Color::parse(value).expect(value);
            assert_eq!((color.red, color.green, color.blue), expected, "{value}");
        }
    }

    #[test]
    fn translucency_and_other_notations_are_still_refused() {
        for value in [
            "rgba(1, 2, 3, 0.5)",
            "rgb(1 2 3 / 20%)",
            "hsla(120, 50%, 50%, 0.5)",
            "lab(50% 40 59.5)",
            "#11223344",
            "currentColor",
            "conflowerblue",
        ] {
            assert!(
                Color::parse(value).is_err(),
                "{value} must be refused, not approximated"
            );
        }
    }

    #[test]
    fn non_finite_channels_are_refused_not_silently_wrong() {
        // "NaN" and "inf" are both syntax f32::from_str accepts, so each
        // counts as parsed, not unparseable, unless checked explicitly.
        // Without that check, a NaN channel bypasses `clamp` (which returns
        // NaN unchanged for a NaN input) and, cast to a pixel channel,
        // silently resolves to 0 rather than being refused the way any
        // other unparseable channel already is.
        for value in [
            "rgb(NaN, 0, 0)",
            "rgb(NaN%, 0, 0)",
            "rgb(inf, 0, 0)",
            "hsl(NaN, 50%, 50%)",
            "hsl(0, NaN%, 50%)",
            "hsl(inf, 50%, 50%)",
        ] {
            assert!(
                Color::parse(value).is_err(),
                "{value} must be refused, not silently resolved to a plausible-but-wrong colour"
            );
        }
    }

    #[test]
    fn parses_a_simple_rule() {
        let sheet = Stylesheet::parse("p { color: red; }").expect("parses");
        assert_eq!(sheet.rules.len(), 1);
        assert_eq!(sheet.rules[0].declarations.len(), 1);
        assert_eq!(sheet.rules[0].declarations[0].property, "color");
        assert_eq!(sheet.rules[0].declarations[0].value, "red");
    }

    #[test]
    fn parses_selector_lists() {
        let sheet = Stylesheet::parse("h1, h2 , h3 { margin: 0 }").expect("parses");
        assert_eq!(sheet.rules[0].selectors.len(), 3);
    }

    #[test]
    fn skips_comments() {
        let sheet = Stylesheet::parse("/* c */ p { color: red }").expect("parses");
        assert_eq!(sheet.rules.len(), 1);
    }

    #[test]
    fn parses_important_flag() {
        let sheet = Stylesheet::parse("p { color: red !important }").expect("parses");
        assert!(sheet.rules[0].declarations[0].important);
        assert_eq!(sheet.rules[0].declarations[0].value, "red");
    }

    #[test]
    fn computes_specificity() {
        let one = parse_selector("#a").expect("parses").specificity();
        let two = parse_selector(".b").expect("parses").specificity();
        let three = parse_selector("div").expect("parses").specificity();
        assert!(one > two && two > three);
        let combined = parse_selector("div.b#a").expect("parses").specificity();
        assert_eq!(
            combined,
            Specificity {
                ids: 1,
                classes: 1,
                types: 1
            }
        );
    }

    #[test]
    fn universal_selector_adds_no_specificity() {
        assert_eq!(
            parse_selector("*").expect("parses").specificity(),
            Specificity::default()
        );
    }

    #[test]
    fn matches_type_class_and_id() {
        assert_eq!(
            declarations("<p class=\"x\" id=\"y\">t</p>", "p { a: 1 }", "p"),
            vec![("a".to_string(), "1".to_string())]
        );
        assert_eq!(
            declarations("<p class=\"x\">t</p>", ".x { a: 1 }", "p"),
            vec![("a".to_string(), "1".to_string())]
        );
        assert_eq!(
            declarations("<p id=\"y\">t</p>", "#y { a: 1 }", "p"),
            vec![("a".to_string(), "1".to_string())]
        );
    }

    #[test]
    fn class_selector_matches_one_of_several_classes() {
        assert_eq!(
            declarations("<p class=\"a b c\">t</p>", ".b { x: 1 }", "p"),
            vec![("x".to_string(), "1".to_string())]
        );
    }

    #[test]
    fn class_selector_does_not_match_a_prefix() {
        // ".b" must not match class="bc"; substring matching here is a classic
        // source of styles leaking onto unrelated elements.
        assert!(declarations("<p class=\"bc\">t</p>", ".b { x: 1 }", "p").is_empty());
    }

    #[test]
    fn matches_descendant_and_child_combinators() {
        let html = "<div><section><p>t</p></section></div>";
        assert_eq!(
            declarations(html, "div p { a: 1 }", "p"),
            vec![("a".to_string(), "1".to_string())]
        );
        // p is a grandchild of div, so the child combinator must not match.
        assert!(declarations(html, "div > p { a: 1 }", "p").is_empty());
        assert_eq!(
            declarations(html, "section > p { a: 1 }", "p"),
            vec![("a".to_string(), "1".to_string())]
        );
    }

    #[test]
    fn matches_sibling_combinators() {
        let html = "<div><h1>h</h1><span>s</span><p>t</p></div>";
        // span immediately precedes p.
        assert_eq!(
            declarations(html, "span + p { a: 1 }", "p"),
            vec![("a".to_string(), "1".to_string())]
        );
        // h1 does not immediately precede p, but does precede it.
        assert!(declarations(html, "h1 + p { a: 1 }", "p").is_empty());
        assert_eq!(
            declarations(html, "h1 ~ p { a: 1 }", "p"),
            vec![("a".to_string(), "1".to_string())]
        );
    }

    #[test]
    fn matches_attribute_selectors() {
        let html = "<a href=\"/x\" data-flag>t</a>";
        assert_eq!(
            declarations(html, "[href] { a: 1 }", "a"),
            vec![("a".to_string(), "1".to_string())]
        );
        assert_eq!(
            declarations(html, "[href=\"/x\"] { a: 1 }", "a"),
            vec![("a".to_string(), "1".to_string())]
        );
        assert!(declarations(html, "[href=\"/other\"] { a: 1 }", "a").is_empty());
        assert_eq!(
            declarations(html, "[data-flag] { a: 1 }", "a"),
            vec![("a".to_string(), "1".to_string())]
        );
    }

    #[test]
    fn higher_specificity_wins() {
        let result = declarations(
            "<p id=\"y\" class=\"x\">t</p>",
            "p { color: red } .x { color: green } #y { color: blue }",
            "p",
        );
        assert_eq!(result, vec![("color".to_string(), "blue".to_string())]);
    }

    #[test]
    fn later_source_order_breaks_specificity_ties() {
        let result = declarations(
            "<p class=\"x\">t</p>",
            ".x { color: red } .x { color: green }",
            "p",
        );
        assert_eq!(result, vec![("color".to_string(), "green".to_string())]);
    }

    #[test]
    fn important_outranks_higher_specificity() {
        // This is the rule most often implemented backwards.
        let result = declarations(
            "<p id=\"y\" class=\"x\">t</p>",
            "#y { color: blue } .x { color: green !important }",
            "p",
        );
        assert_eq!(result, vec![("color".to_string(), "green".to_string())]);
    }

    #[test]
    fn non_matching_rules_contribute_nothing() {
        assert!(declarations("<p>t</p>", "div { color: red }", "p").is_empty());
    }

    #[test]
    fn at_rules_are_reported_not_ignored() {
        let error = Stylesheet::parse("@media screen { p { color: red } }").expect_err("refused");
        assert!(matches!(error, CssError::AtRuleUnsupported { .. }));
    }

    #[test]
    fn pseudo_classes_are_reported_not_ignored() {
        let error = Stylesheet::parse("p:nth-child(2) { color: red }").expect_err("refused");
        assert!(matches!(error, CssError::PseudoClassUnsupported { .. }));
    }

    #[test]
    fn hover_matches_only_the_hovered_element() {
        let doc = document("<p>t</p>");
        let sheet = Stylesheet::parse("p:hover { color: red }").expect("parses");
        let index = SelectorIndex::build(&sheet);
        let p = find(&doc, "p");

        assert!(
            cascade(&doc, p, &index, None).is_empty(),
            "nothing is hovered, so :hover must not match"
        );
        assert_eq!(
            cascade(&doc, p, &index, Some(p)),
            cascade_reference(&doc, p, &sheet, Some(p)),
            "indexed and reference cascades must agree once hover is involved too"
        );
        assert_eq!(
            cascade(&doc, p, &index, Some(p)),
            vec![(
                "color".to_string(),
                ComputedDeclaration {
                    value: "red".to_string(),
                    important: false,
                    specificity: Specificity {
                        ids: 0,
                        classes: 1,
                        types: 1,
                    },
                    source_order: 0,
                }
            )]
        );
    }

    #[test]
    fn hover_on_an_ancestor_compound_still_matches() {
        // `.parent:hover .child` — the hovered element is the ancestor, not
        // the subject, so the hover check has to run for every compound in
        // the selector, not only the rightmost one.
        let doc = document("<div class=\"parent\"><p>t</p></div>");
        let sheet = Stylesheet::parse(".parent:hover p { color: red }").expect("parses");
        let index = SelectorIndex::build(&sheet);
        let p = find(&doc, "p");
        let div = find(&doc, "div");

        assert!(cascade(&doc, p, &index, None).is_empty());
        assert!(
            cascade(&doc, p, &index, Some(p)).is_empty(),
            "the paragraph itself being hovered does not satisfy .parent:hover"
        );
        assert_eq!(
            cascade(&doc, p, &index, Some(div)),
            vec![(
                "color".to_string(),
                ComputedDeclaration {
                    value: "red".to_string(),
                    important: false,
                    // `.parent` and `:hover` both count as class-level
                    // (classes: 2), plus the `p` type compound (types: 1).
                    specificity: Specificity {
                        ids: 0,
                        classes: 2,
                        types: 1,
                    },
                    source_order: 0,
                }
            )]
        );
    }

    #[test]
    fn hover_pseudo_class_is_not_reported_as_unsupported() {
        // Every other single-colon pseudo-class is refused (see
        // `pseudo_classes_are_reported_not_ignored`); `:hover` is the one
        // exception, so parsing it must succeed rather than error.
        Stylesheet::parse("a:hover { color: red }").expect("hover is a supported pseudo-class");
    }

    #[test]
    fn pseudo_elements_are_reported_not_ignored() {
        let error = Stylesheet::parse("p::before { content: \"x\" }").expect_err("refused");
        assert!(matches!(error, CssError::PseudoElementUnsupported { .. }));
    }

    #[test]
    fn unterminated_block_is_reported() {
        let error = Stylesheet::parse("p { color: red").expect_err("refused");
        assert!(matches!(error, CssError::UnterminatedBlock { .. }));
    }

    #[test]
    fn malformed_declarations_are_dropped_not_fatal() {
        // Error recovery inside a block is specified behavior, unlike an
        // unmodeled selector, which changes what matches.
        let sheet = Stylesheet::parse("p { color red; margin: 0 }").expect("parses");
        assert_eq!(sheet.rules[0].declarations.len(), 1);
        assert_eq!(sheet.rules[0].declarations[0].property, "margin");
    }

    #[test]
    fn styles_a_small_page_end_to_end() {
        let html = "<div id=\"main\"><p class=\"lead\">hello</p><p>other</p></div>";
        let css = "p { color: black; margin: 1px } \
                   #main .lead { color: red } \
                   p { margin: 2px }";
        let result = declarations(html, css, "p");
        assert_eq!(
            result,
            vec![
                ("color".to_string(), "red".to_string()),
                ("margin".to_string(), "2px".to_string()),
            ]
        );
    }

    // -- custom properties and var() -------------------------------------
    //
    // These stylesheets declare a custom property on a plain class selector
    // rather than `:root`. `:root` itself is a pseudo-class this crate does
    // not evaluate (`PseudoClassUnsupported`, matching every structural or
    // functional pseudo-class other than `:hover`) — a separate, pre-existing
    // gap this task does not close. A class on the tree's outermost element
    // plays the same role for these tests: something broad that a deep
    // descendant inherits through.

    #[test]
    fn custom_property_names_preserve_case_but_standard_property_names_do_not() {
        // Custom properties are case-sensitive (`--Ink` and `--ink` would be
        // different properties); standard properties are ASCII
        // case-insensitive, so `COLOR` must still fold to `color`.
        let sheet = Stylesheet::parse("p { --Ink: not-a-real-color; COLOR: red; }")
            .expect("parses even though --Ink's value is never validated as a colour");
        let declarations = &sheet.rules[0].declarations;
        assert_eq!(declarations[0].property, "--Ink");
        assert_eq!(declarations[0].value, "not-a-real-color");
        assert_eq!(declarations[1].property, "color");
    }

    #[test]
    fn var_resolves_to_the_root_declared_value_from_a_deep_descendant() {
        let html = "<div class=\"root\"><section><article><p>t</p></article></section></div>";
        let css = ".root { --ac: blue; } p { color: var(--ac); }";
        assert_eq!(
            resolved_declarations(html, css, "p").expect("resolves"),
            vec![("color".to_string(), "blue".to_string())]
        );
    }

    #[test]
    fn var_fallback_is_used_when_the_custom_property_is_undefined() {
        let html = "<p>t</p>";
        let css = "p { color: var(--missing, green); }";
        assert_eq!(
            resolved_declarations(html, css, "p").expect("resolves via fallback"),
            vec![("color".to_string(), "green".to_string())]
        );
    }

    #[test]
    fn undefined_custom_property_with_no_fallback_is_refused() {
        let html = "<p>t</p>";
        let css = "p { color: var(--missing); }";
        let error = resolved_declarations(html, css, "p").expect_err("must be refused");
        assert_eq!(
            error,
            CssError::CustomPropertyUndefined {
                name: "--missing".to_string()
            }
        );
    }

    #[test]
    fn a_more_specific_rule_overrides_the_custom_property_and_var_sees_the_winner() {
        // `#y` outranks `.root` on specificity, on the same element, so the
        // custom property's own cascade must pick `blue` before `var()` ever
        // runs — the same rule that governs any other property.
        let html = "<div class=\"root\" id=\"y\"><p>t</p></div>";
        let css = ".root { --ac: red; } #y { --ac: blue; } p { color: var(--ac); }";
        assert_eq!(
            resolved_declarations(html, css, "p").expect("resolves"),
            vec![("color".to_string(), "blue".to_string())]
        );
    }

    #[test]
    fn a_later_rule_of_equal_specificity_overrides_the_custom_property_and_var_sees_the_winner() {
        let html = "<div class=\"root\"><p>t</p></div>";
        let css = ".root { --ac: red; } .root { --ac: green; } p { color: var(--ac); }";
        assert_eq!(
            resolved_declarations(html, css, "p").expect("resolves"),
            vec![("color".to_string(), "green".to_string())]
        );
    }

    #[test]
    fn nested_var_fallback_falls_through_to_the_innermost_default() {
        // `var(--a, var(--b, red))`, with neither `--a` nor `--b` declared
        // anywhere: this is the nesting shape the task calls out by name, and
        // it must resolve soundly to the literal fallback, not error or
        // truncate.
        let html = "<p>t</p>";
        let css = "p { color: var(--a, var(--b, red)); }";
        assert_eq!(
            resolved_declarations(html, css, "p").expect("resolves"),
            vec![("color".to_string(), "red".to_string())]
        );
    }

    #[test]
    fn nested_var_fallback_picks_up_an_inherited_inner_custom_property() {
        // Same shape as above, but `--b` is declared on an ancestor, so the
        // inner `var()` inside the fallback must resolve through the
        // environment rather than only ever falling through to `red`.
        let html = "<div class=\"root\"><p>t</p></div>";
        let css = ".root { --b: teal; } p { color: var(--a, var(--b, red)); }";
        assert_eq!(
            resolved_declarations(html, css, "p").expect("resolves"),
            vec![("color".to_string(), "teal".to_string())]
        );
    }

    #[test]
    fn a_custom_property_chain_through_var_resolves_transitively() {
        // `--gap` is not used directly; `width` uses `--space`, whose own
        // (unresolved, stored) value is `var(--gap)`. Resolution has to
        // follow that chain, not stop at the first substitution.
        let html = "<div class=\"root\"><p>t</p></div>";
        let css = ".root { --gap: 8px; --space: var(--gap); } p { width: var(--space); }";
        assert_eq!(
            resolved_declarations(html, css, "p").expect("resolves"),
            vec![("width".to_string(), "8px".to_string())]
        );
    }

    #[test]
    fn malformed_var_calls_are_refused_not_panicking() {
        for value in [
            "var()",        // no arguments at all
            "var(--)",      // empty custom property name
            "var(  , red)", // blank name before the fallback comma
            "var(color)",   // not a custom property (no `--` prefix)
            "var(--x",      // unterminated: no closing parenthesis
        ] {
            let html = "<p>t</p>";
            let css = format!("p {{ color: {value}; }}");
            let error = resolved_declarations(html, &css, "p")
                .expect_err(&format!("{value} must be refused, not panic"));
            assert!(
                matches!(error, CssError::CustomPropertySyntax { .. }),
                "{value} produced {error:?}, expected CustomPropertySyntax"
            );
        }
    }

    #[test]
    fn var_nesting_past_the_bound_is_refused_rather_than_recursing_forever() {
        // Neither declared anywhere: each level falls through to the next,
        // recursing one level deeper per `var()`, until the depth bound is
        // exceeded. Whether this comes from an honestly deep design-token
        // chain or a cyclic custom property makes no difference to the
        // implementation — both must terminate, not overflow the stack.
        let mut value = "red".to_string();
        for level in 0..40 {
            value = format!("var(--x{level}, {value})");
        }
        let html = "<p>t</p>";
        let css = format!("p {{ color: {value}; }}");
        let error = resolved_declarations(html, &css, "p").expect_err("must be refused");
        assert!(matches!(
            error,
            CssError::CustomPropertyNestingTooDeep { .. }
        ));
    }

    #[test]
    fn custom_property_declarations_pass_through_unresolved() {
        // Resolution is scoped to standard properties that reference a
        // custom property via var(); a custom property's own stored value is
        // returned verbatim, unparsed, matching this crate's wider policy of
        // never validating a value until something asks to interpret it.
        let html = "<p>t</p>";
        let css = "p { --raw: var(--never-declared, still not validated here); }";
        assert_eq!(
            resolved_declarations(html, css, "p")
                .expect("the custom property itself is not resolved"),
            vec![(
                "--raw".to_string(),
                "var(--never-declared, still not validated here)".to_string()
            )]
        );
    }
}
