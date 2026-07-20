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

#![forbid(unsafe_code)]

use core::fmt;
use turing_html::{Document, NodeData, NodeId};

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
                    | SimpleSelector::AttributeEquals { .. } => total.classes += 1,
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
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Declaration {
    /// Lowercased property name.
    pub property: String,
    /// Value text, unparsed. Value parsing is per-property and belongs to the
    /// property implementations, not the syntax layer.
    pub value: String,
    /// Whether `!important` was present.
    pub important: bool,
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
                // matching, so both are refused rather than dropped.
                let double = bytes.get(index + 1) == Some(&b':');
                let start = if double { index + 2 } else { index + 1 };
                let (name, _) = read_ident(bytes, start);
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
        let property = property.trim().to_ascii_lowercase();
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

/// Returns whether `selector` matches `element` in `document`.
#[must_use]
pub fn matches(document: &Document, element: NodeId, selector: &Selector) -> bool {
    if !compound_matches(document, element, &selector.subject) {
        return false;
    }
    let mut current = element;
    for (combinator, compound) in &selector.ancestors {
        match combinator {
            Combinator::Descendant => match find_ancestor(document, current, compound) {
                Some(found) => current = found,
                None => return false,
            },
            Combinator::Child => {
                let Some(parent) = document.node(current).parent else {
                    return false;
                };
                if !compound_matches(document, parent, compound) {
                    return false;
                }
                current = parent;
            }
            Combinator::NextSibling => {
                let Some(previous) = previous_element_sibling(document, current) else {
                    return false;
                };
                if !compound_matches(document, previous, compound) {
                    return false;
                }
                current = previous;
            }
            Combinator::SubsequentSibling => {
                let mut cursor = previous_element_sibling(document, current);
                let mut found = None;
                while let Some(candidate) = cursor {
                    if compound_matches(document, candidate, compound) {
                        found = Some(candidate);
                        break;
                    }
                    cursor = previous_element_sibling(document, candidate);
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

fn find_ancestor(document: &Document, from: NodeId, compound: &Compound) -> Option<NodeId> {
    let mut cursor = document.node(from).parent;
    while let Some(candidate) = cursor {
        if compound_matches(document, candidate, compound) {
            return Some(candidate);
        }
        cursor = document.node(candidate).parent;
    }
    None
}

fn previous_element_sibling(document: &Document, node: NodeId) -> Option<NodeId> {
    let parent = document.node(node).parent?;
    let siblings = &document.node(parent).children;
    let index = siblings.iter().position(|&id| id == node)?;
    siblings[..index]
        .iter()
        .rev()
        .copied()
        .find(|&id| matches!(document.node(id).data, NodeData::Element { .. }))
}

fn compound_matches(document: &Document, element: NodeId, compound: &Compound) -> bool {
    let NodeData::Element { name, attributes } = &document.node(element).data else {
        return false;
    };
    compound.parts.iter().all(|part| match part {
        SimpleSelector::Universal => true,
        SimpleSelector::Type(expected) => name == expected,
        SimpleSelector::Class(expected) => attributes
            .iter()
            .find(|attribute| attribute.name == "class")
            .is_some_and(|attribute| attribute.value.split_whitespace().any(|c| c == expected)),
        SimpleSelector::Id(expected) => attributes
            .iter()
            .any(|attribute| attribute.name == "id" && attribute.value == *expected),
        SimpleSelector::AttributePresent(expected) => attributes
            .iter()
            .any(|attribute| attribute.name == *expected),
        SimpleSelector::AttributeEquals { name: key, value } => attributes
            .iter()
            .any(|attribute| attribute.name == *key && attribute.value == *value),
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
pub fn cascade(
    document: &Document,
    element: NodeId,
    stylesheet: &Stylesheet,
) -> Vec<(String, ComputedDeclaration)> {
    let mut winners: Vec<(String, ComputedDeclaration)> = Vec::new();

    for (order, rule) in stylesheet.rules.iter().enumerate() {
        let Some(specificity) = rule
            .selectors
            .iter()
            .filter(|selector| matches(document, element, selector))
            .map(Selector::specificity)
            .max()
        else {
            continue;
        };
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

#[cfg(test)]
mod tests {
    use super::*;
    use turing_html::{Tokenizer, TreeBuilder};

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
        cascade(&doc, find(&doc, element), &sheet)
            .into_iter()
            .map(|(property, computed)| (property, computed.value))
            .collect()
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
}
