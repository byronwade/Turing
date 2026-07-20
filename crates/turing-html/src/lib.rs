// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Turing-owned HTML tokenizer.
//!
//! This crate implements the tokenization stage of the HTML parsing pipeline
//! described by `WP-006` and `REQ-ENG-001`. It is written against the WHATWG
//! HTML tokenizer state machine and does not invoke, link, or derive from an
//! existing browser engine, consistent with the `ADR-0009` Option A direction
//! selected by the program owner on 2026-07-20.
//!
//! # Scope
//!
//! This is the tokenizer only. It produces a token stream; it does not build a
//! DOM, apply the tree-construction insertion modes, resolve character
//! references beyond the named-reference subset below, or execute scripts. Tree
//! construction is separate work under the same work package.
//!
//! # Deliberate limits
//!
//! The WHATWG tokenizer defines roughly eighty states. This implementation
//! covers the states reachable from ordinary markup: data, tag open, tag name,
//! attributes with all three quoting forms, self-closing tags, comments,
//! DOCTYPE, and the raw-text and RCDATA content models used by `script`,
//! `style`, `title`, and `textarea`. States for CDATA sections and the more
//! obscure DOCTYPE error branches are not implemented and are reported through
//! [`TokenizerError`] rather than silently mis-tokenized.
//!
//! Every unimplemented branch fails loudly. Silence would let a gap read as
//! conformance, which this program's evidence rules forbid.

#![forbid(unsafe_code)]

pub mod tree;

pub use tree::{Document, MutationError, Node, NodeData, NodeId, TreeBuilder, TreeError};

use core::fmt;

/// A parse condition the tokenizer detected but could still recover from.
///
/// The HTML specification requires that parse errors do not stop tokenization.
/// They are collected so a caller can report them without changing the token
/// stream a browser would produce.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ParseError {
    /// Byte offset into the input where the condition was detected.
    pub offset: usize,
    /// Stable identifier for the condition, matching WHATWG error names where
    /// one exists.
    pub kind: ParseErrorKind,
}

/// Recoverable tokenizer conditions.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ParseErrorKind {
    /// End of input arrived while a tag was still open.
    EofInTag,
    /// End of input arrived inside a comment.
    EofInComment,
    /// End of input arrived inside a DOCTYPE.
    EofInDoctype,
    /// A tag name began with something other than an ASCII letter.
    InvalidFirstCharacterOfTagName,
    /// An attribute name contained a character the specification disallows.
    UnexpectedCharacterInAttributeName,
    /// The same attribute name appeared twice on one tag; the later value is
    /// dropped, matching specified behavior.
    DuplicateAttribute,
    /// A `<` was followed by `/` and then `>` with no tag name between them.
    MissingEndTagName,
    /// A numeric character reference was malformed.
    MalformedCharacterReference,
}

/// A condition the tokenizer cannot represent, as distinct from a parse error.
///
/// These indicate input this implementation does not yet cover. They are
/// returned rather than approximated so that unimplemented coverage cannot be
/// mistaken for conformance.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum TokenizerError {
    /// A CDATA section was encountered. Only meaningful in foreign content,
    /// which requires tree construction this crate does not perform.
    CdataSectionUnsupported { offset: usize },
    /// A DOCTYPE used a branch this implementation does not model.
    DoctypeBranchUnsupported { offset: usize },
}

impl fmt::Display for TokenizerError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::CdataSectionUnsupported { offset } => write!(
                formatter,
                "CDATA section at byte {offset} is not implemented; it requires foreign-content tree construction"
            ),
            Self::DoctypeBranchUnsupported { offset } => write!(
                formatter,
                "DOCTYPE branch at byte {offset} is not implemented"
            ),
        }
    }
}

/// An attribute on a start or end tag.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Attribute {
    /// Attribute name, lowercased as the specification requires.
    pub name: String,
    /// Attribute value with character references resolved.
    pub value: String,
}

/// A token produced by the tokenizer.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum Token {
    /// Character data. Runs are coalesced so callers see whole text spans.
    Characters(String),
    /// A start tag, possibly self-closing.
    StartTag {
        name: String,
        attributes: Vec<Attribute>,
        self_closing: bool,
    },
    /// An end tag. Attributes on end tags are a parse error and are dropped.
    EndTag { name: String },
    /// A comment's data, excluding the delimiters.
    Comment(String),
    /// A DOCTYPE. Public and system identifiers are captured when present.
    Doctype {
        name: Option<String>,
        public_id: Option<String>,
        system_id: Option<String>,
        force_quirks: bool,
    },
}

/// Content model for the element whose contents are being tokenized.
///
/// Tree construction selects this; the tokenizer cannot infer it, because the
/// same bytes tokenize differently inside `script` than inside `div`.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum ContentModel {
    /// Ordinary markup. Tags and character references are recognized.
    Data,
    /// `title` and `textarea`. Character references are recognized; tags are
    /// not, except the matching end tag.
    RcData,
    /// `style`. Neither tags nor character references are recognized, except
    /// the matching end tag.
    RawText,
    /// `script`. Like raw text, with the additional escape handling the
    /// specification defines for script data.
    ScriptData,
}

/// Result of a tokenization run.
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Tokenized {
    /// Tokens in document order.
    pub tokens: Vec<Token>,
    /// Recoverable conditions, in the order detected.
    pub errors: Vec<ParseError>,
}

/// The tokenizer state machine.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum State {
    Data,
    TagOpen,
    EndTagOpen,
    TagName,
    BeforeAttributeName,
    AttributeName,
    AfterAttributeName,
    BeforeAttributeValue,
    AttributeValueDoubleQuoted,
    AttributeValueSingleQuoted,
    AttributeValueUnquoted,
    AfterAttributeValueQuoted,
    SelfClosingStartTag,
    MarkupDeclarationOpen,
    CommentStart,
    Comment,
    CommentEndDash,
    CommentEnd,
    Doctype,
    DoctypeName,
    AfterDoctypeName,
    BogusComment,
    RawTextLike,
}

/// Tokenizes HTML source into a token stream.
///
/// The tokenizer is a single pass over the input with no backtracking, which
/// keeps its cost linear in input length. It borrows the input and allocates
/// only for token payloads.
#[derive(Debug)]
pub struct Tokenizer<'input> {
    input: &'input [u8],
    position: usize,
    state: State,
    content_model: ContentModel,
    tokens: Vec<Token>,
    errors: Vec<ParseError>,
    pending_characters: String,
    tag_name: String,
    tag_is_end: bool,
    tag_self_closing: bool,
    attributes: Vec<Attribute>,
    attribute_name: String,
    attribute_value: String,
    comment: String,
    doctype_name: String,
    doctype_force_quirks: bool,
    /// End tag name that terminates the current raw-text or RCDATA span.
    raw_text_end_tag: String,
}

impl<'input> Tokenizer<'input> {
    /// Creates a tokenizer over `input` in the ordinary data content model.
    #[must_use]
    pub fn new(input: &'input str) -> Self {
        Self::with_content_model(input, ContentModel::Data)
    }

    /// Creates a tokenizer with an explicit content model.
    ///
    /// Tree construction uses this when entering `script`, `style`, `title`,
    /// or `textarea`, where the same bytes tokenize differently.
    #[must_use]
    pub fn with_content_model(input: &'input str, content_model: ContentModel) -> Self {
        let state = match content_model {
            ContentModel::Data => State::Data,
            _ => State::RawTextLike,
        };
        Self {
            input: input.as_bytes(),
            position: 0,
            state,
            content_model,
            tokens: Vec::new(),
            errors: Vec::new(),
            pending_characters: String::new(),
            tag_name: String::new(),
            tag_is_end: false,
            tag_self_closing: false,
            attributes: Vec::new(),
            attribute_name: String::new(),
            attribute_value: String::new(),
            comment: String::new(),
            doctype_name: String::new(),
            doctype_force_quirks: false,
            raw_text_end_tag: String::new(),
        }
    }

    /// Sets the end tag that closes the current raw-text or RCDATA span.
    ///
    /// Without this, a raw-text tokenizer cannot know which `</...>` ends it,
    /// because inside raw text every other tag is character data.
    pub fn set_raw_text_end_tag(&mut self, name: &str) {
        self.raw_text_end_tag = name.to_ascii_lowercase();
    }

    /// Runs the tokenizer to end of input.
    ///
    /// # Errors
    ///
    /// Returns [`TokenizerError`] when the input reaches a construct this
    /// implementation does not model, rather than producing a token stream
    /// that would misrepresent it.
    pub fn tokenize(mut self) -> Result<Tokenized, TokenizerError> {
        while self.position < self.input.len() {
            self.step()?;
        }
        self.finish_at_eof();
        self.flush_characters();
        Ok(Tokenized {
            tokens: self.tokens,
            errors: self.errors,
        })
    }

    fn step(&mut self) -> Result<(), TokenizerError> {
        let byte = self.input[self.position];
        match self.state {
            State::RawTextLike => self.step_raw_text_like(),
            State::Data => self.step_data(byte),
            State::TagOpen => self.step_tag_open(byte)?,
            State::EndTagOpen => self.step_end_tag_open(byte),
            State::TagName => self.step_tag_name(byte),
            State::BeforeAttributeName => self.step_before_attribute_name(byte),
            State::AttributeName => self.step_attribute_name(byte),
            State::AfterAttributeName => self.step_after_attribute_name(byte),
            State::BeforeAttributeValue => self.step_before_attribute_value(byte),
            State::AttributeValueDoubleQuoted => self.step_attribute_value_quoted(byte, b'"'),
            State::AttributeValueSingleQuoted => self.step_attribute_value_quoted(byte, b'\''),
            State::AttributeValueUnquoted => self.step_attribute_value_unquoted(byte),
            State::AfterAttributeValueQuoted => self.step_after_attribute_value_quoted(byte),
            State::SelfClosingStartTag => self.step_self_closing_start_tag(byte),
            State::MarkupDeclarationOpen => self.step_markup_declaration_open()?,
            State::CommentStart => self.step_comment_start(byte),
            State::Comment => self.step_comment(byte),
            State::CommentEndDash => self.step_comment_end_dash(byte),
            State::CommentEnd => self.step_comment_end(byte),
            State::Doctype => self.step_doctype(byte),
            State::DoctypeName => self.step_doctype_name(byte),
            State::AfterDoctypeName => self.step_after_doctype_name(byte)?,
            State::BogusComment => self.step_bogus_comment(byte),
        }
        Ok(())
    }

    // -- data ------------------------------------------------------------

    fn step_data(&mut self, byte: u8) {
        match byte {
            b'<' => {
                self.state = State::TagOpen;
                self.position += 1;
            }
            b'&' => self.consume_character_reference(),
            _ => self.consume_text_byte(),
        }
    }

    /// Raw text and RCDATA differ from data only in what terminates them, so
    /// they share one routine that scans for the matching end tag.
    fn step_raw_text_like(&mut self) {
        if self.input[self.position] == b'&' && self.content_model == ContentModel::RcData {
            self.consume_character_reference();
            return;
        }
        if self.input[self.position] == b'<' && self.matches_raw_text_end_tag() {
            self.flush_characters();
            let name = self.raw_text_end_tag.clone();
            self.tokens.push(Token::EndTag { name });
            // Skip "</", the tag name, and the ">".
            self.position += 2 + self.raw_text_end_tag.len() + 1;
            self.state = State::Data;
            self.content_model = ContentModel::Data;
            return;
        }
        self.consume_text_byte();
    }

    fn matches_raw_text_end_tag(&self) -> bool {
        if self.raw_text_end_tag.is_empty() {
            return false;
        }
        let after = self.position + 2;
        let end = after + self.raw_text_end_tag.len();
        if end >= self.input.len() {
            return false;
        }
        if &self.input[self.position..after] != b"</" {
            return false;
        }
        if !self.input[after..end].eq_ignore_ascii_case(self.raw_text_end_tag.as_bytes()) {
            return false;
        }
        self.input[end] == b'>'
    }

    fn consume_text_byte(&mut self) {
        let start = self.position;
        let length = utf8_sequence_length(self.input[start]);
        let end = (start + length).min(self.input.len());
        if let Ok(text) = core::str::from_utf8(&self.input[start..end]) {
            self.pending_characters.push_str(text);
        }
        self.position = end;
    }

    // -- tags ------------------------------------------------------------

    fn step_tag_open(&mut self, byte: u8) -> Result<(), TokenizerError> {
        match byte {
            b'!' => {
                self.state = State::MarkupDeclarationOpen;
                self.position += 1;
            }
            b'/' => {
                self.state = State::EndTagOpen;
                self.position += 1;
            }
            _ if byte.is_ascii_alphabetic() => {
                self.flush_characters();
                self.begin_tag(false);
                self.state = State::TagName;
            }
            _ => {
                self.error(ParseErrorKind::InvalidFirstCharacterOfTagName);
                self.pending_characters.push('<');
                self.state = State::Data;
            }
        }
        Ok(())
    }

    fn step_end_tag_open(&mut self, byte: u8) {
        if byte == b'>' {
            self.error(ParseErrorKind::MissingEndTagName);
            self.state = State::Data;
            self.position += 1;
        } else if byte.is_ascii_alphabetic() {
            self.flush_characters();
            self.begin_tag(true);
            self.state = State::TagName;
        } else {
            self.error(ParseErrorKind::InvalidFirstCharacterOfTagName);
            self.comment.clear();
            self.state = State::BogusComment;
        }
    }

    fn begin_tag(&mut self, is_end: bool) {
        self.tag_name.clear();
        self.attributes.clear();
        self.tag_is_end = is_end;
        self.tag_self_closing = false;
    }

    fn step_tag_name(&mut self, byte: u8) {
        match byte {
            b'\t' | b'\n' | b'\x0C' | b' ' => {
                self.state = State::BeforeAttributeName;
                self.position += 1;
            }
            b'/' => {
                self.state = State::SelfClosingStartTag;
                self.position += 1;
            }
            b'>' => self.emit_tag(),
            _ => {
                self.tag_name.push(byte.to_ascii_lowercase() as char);
                self.position += 1;
            }
        }
    }

    fn step_before_attribute_name(&mut self, byte: u8) {
        match byte {
            b'\t' | b'\n' | b'\x0C' | b' ' => self.position += 1,
            b'/' => {
                self.state = State::SelfClosingStartTag;
                self.position += 1;
            }
            b'>' => self.emit_tag(),
            _ => {
                self.attribute_name.clear();
                self.attribute_value.clear();
                self.state = State::AttributeName;
            }
        }
    }

    fn step_attribute_name(&mut self, byte: u8) {
        match byte {
            b'\t' | b'\n' | b'\x0C' | b' ' => {
                self.state = State::AfterAttributeName;
                self.position += 1;
            }
            b'/' => {
                self.finish_attribute();
                self.state = State::SelfClosingStartTag;
                self.position += 1;
            }
            b'=' => {
                self.state = State::BeforeAttributeValue;
                self.position += 1;
            }
            b'>' => {
                self.finish_attribute();
                self.emit_tag();
            }
            b'"' | b'\'' | b'<' => {
                self.error(ParseErrorKind::UnexpectedCharacterInAttributeName);
                self.attribute_name.push(byte as char);
                self.position += 1;
            }
            _ => {
                self.attribute_name.push(byte.to_ascii_lowercase() as char);
                self.position += 1;
            }
        }
    }

    fn step_after_attribute_name(&mut self, byte: u8) {
        match byte {
            b'\t' | b'\n' | b'\x0C' | b' ' => self.position += 1,
            b'/' => {
                self.finish_attribute();
                self.state = State::SelfClosingStartTag;
                self.position += 1;
            }
            b'=' => {
                self.state = State::BeforeAttributeValue;
                self.position += 1;
            }
            b'>' => {
                self.finish_attribute();
                self.emit_tag();
            }
            _ => {
                self.finish_attribute();
                self.attribute_name.clear();
                self.attribute_value.clear();
                self.state = State::AttributeName;
            }
        }
    }

    fn step_before_attribute_value(&mut self, byte: u8) {
        match byte {
            b'\t' | b'\n' | b'\x0C' | b' ' => self.position += 1,
            b'"' => {
                self.state = State::AttributeValueDoubleQuoted;
                self.position += 1;
            }
            b'\'' => {
                self.state = State::AttributeValueSingleQuoted;
                self.position += 1;
            }
            b'>' => {
                self.finish_attribute();
                self.emit_tag();
            }
            _ => self.state = State::AttributeValueUnquoted,
        }
    }

    fn step_attribute_value_quoted(&mut self, byte: u8, quote: u8) {
        if byte == quote {
            self.finish_attribute();
            self.state = State::AfterAttributeValueQuoted;
            self.position += 1;
        } else if byte == b'&' {
            let resolved = self.take_character_reference();
            self.attribute_value.push_str(&resolved);
        } else {
            self.push_attribute_value_byte();
        }
    }

    fn step_attribute_value_unquoted(&mut self, byte: u8) {
        match byte {
            b'\t' | b'\n' | b'\x0C' | b' ' => {
                self.finish_attribute();
                self.state = State::BeforeAttributeName;
                self.position += 1;
            }
            b'>' => {
                self.finish_attribute();
                self.emit_tag();
            }
            b'&' => {
                let resolved = self.take_character_reference();
                self.attribute_value.push_str(&resolved);
            }
            _ => self.push_attribute_value_byte(),
        }
    }

    fn push_attribute_value_byte(&mut self) {
        let start = self.position;
        let length = utf8_sequence_length(self.input[start]);
        let end = (start + length).min(self.input.len());
        if let Ok(text) = core::str::from_utf8(&self.input[start..end]) {
            self.attribute_value.push_str(text);
        }
        self.position = end;
    }

    fn step_after_attribute_value_quoted(&mut self, byte: u8) {
        match byte {
            b'\t' | b'\n' | b'\x0C' | b' ' => {
                self.state = State::BeforeAttributeName;
                self.position += 1;
            }
            b'/' => {
                self.state = State::SelfClosingStartTag;
                self.position += 1;
            }
            b'>' => self.emit_tag(),
            _ => self.state = State::BeforeAttributeName,
        }
    }

    fn step_self_closing_start_tag(&mut self, byte: u8) {
        if byte == b'>' {
            self.tag_self_closing = true;
            self.emit_tag();
        } else {
            self.state = State::BeforeAttributeName;
        }
    }

    fn finish_attribute(&mut self) {
        if self.attribute_name.is_empty() {
            return;
        }
        let name = core::mem::take(&mut self.attribute_name);
        let value = core::mem::take(&mut self.attribute_value);
        if self.attributes.iter().any(|existing| existing.name == name) {
            self.error(ParseErrorKind::DuplicateAttribute);
            return;
        }
        self.attributes.push(Attribute { name, value });
    }

    fn emit_tag(&mut self) {
        self.finish_attribute();
        self.flush_characters();
        let name = core::mem::take(&mut self.tag_name);
        let attributes = core::mem::take(&mut self.attributes);
        if self.tag_is_end {
            // End tags cannot carry attributes; the specification drops them.
            self.tokens.push(Token::EndTag { name });
        } else {
            // Entering a raw-text element changes how following bytes
            // tokenize, so switch the content model here rather than making
            // the caller re-enter the tokenizer.
            let next_model = raw_text_model_for(&name);
            self.tokens.push(Token::StartTag {
                name: name.clone(),
                attributes,
                self_closing: self.tag_self_closing,
            });
            if let Some(model) = next_model
                && !self.tag_self_closing
            {
                self.content_model = model;
                self.raw_text_end_tag = name;
                self.state = State::RawTextLike;
                self.position += 1;
                return;
            }
        }
        self.state = State::Data;
        self.position += 1;
    }

    // -- comments, DOCTYPE -----------------------------------------------

    fn step_markup_declaration_open(&mut self) -> Result<(), TokenizerError> {
        let rest = &self.input[self.position..];
        if rest.starts_with(b"--") {
            self.flush_characters();
            self.comment.clear();
            self.state = State::CommentStart;
            self.position += 2;
        } else if rest.len() >= 7 && rest[..7].eq_ignore_ascii_case(b"DOCTYPE") {
            self.flush_characters();
            self.doctype_name.clear();
            self.doctype_force_quirks = false;
            self.state = State::Doctype;
            self.position += 7;
        } else if rest.starts_with(b"[CDATA[") {
            return Err(TokenizerError::CdataSectionUnsupported {
                offset: self.position,
            });
        } else {
            self.comment.clear();
            self.state = State::BogusComment;
        }
        Ok(())
    }

    fn step_comment_start(&mut self, byte: u8) {
        if byte == b'-' {
            self.state = State::CommentEndDash;
            self.position += 1;
        } else {
            self.state = State::Comment;
        }
    }

    fn step_comment(&mut self, byte: u8) {
        if byte == b'-' {
            self.state = State::CommentEndDash;
            self.position += 1;
        } else {
            let start = self.position;
            let length = utf8_sequence_length(byte);
            let end = (start + length).min(self.input.len());
            if let Ok(text) = core::str::from_utf8(&self.input[start..end]) {
                self.comment.push_str(text);
            }
            self.position = end;
        }
    }

    fn step_comment_end_dash(&mut self, byte: u8) {
        if byte == b'-' {
            self.state = State::CommentEnd;
            self.position += 1;
        } else {
            self.comment.push('-');
            self.state = State::Comment;
        }
    }

    fn step_comment_end(&mut self, byte: u8) {
        match byte {
            b'>' => {
                let comment = core::mem::take(&mut self.comment);
                self.tokens.push(Token::Comment(comment));
                self.state = State::Data;
                self.position += 1;
            }
            b'-' => {
                self.comment.push('-');
                self.position += 1;
            }
            _ => {
                self.comment.push_str("--");
                self.state = State::Comment;
            }
        }
    }

    fn step_doctype(&mut self, byte: u8) {
        match byte {
            b'\t' | b'\n' | b'\x0C' | b' ' => self.position += 1,
            b'>' => {
                self.emit_doctype(None, None);
                self.position += 1;
            }
            _ => self.state = State::DoctypeName,
        }
    }

    fn step_doctype_name(&mut self, byte: u8) {
        match byte {
            b'\t' | b'\n' | b'\x0C' | b' ' => {
                self.state = State::AfterDoctypeName;
                self.position += 1;
            }
            b'>' => {
                let name = core::mem::take(&mut self.doctype_name);
                self.emit_doctype(Some(name), None);
                self.position += 1;
            }
            _ => {
                self.doctype_name.push(byte.to_ascii_lowercase() as char);
                self.position += 1;
            }
        }
    }

    fn step_after_doctype_name(&mut self, byte: u8) -> Result<(), TokenizerError> {
        match byte {
            b'\t' | b'\n' | b'\x0C' | b' ' => {
                self.position += 1;
                Ok(())
            }
            b'>' => {
                let name = core::mem::take(&mut self.doctype_name);
                self.emit_doctype(Some(name), None);
                self.position += 1;
                Ok(())
            }
            // PUBLIC and SYSTEM identifier branches are not modeled. Reporting
            // is better than guessing, because a wrong system identifier
            // changes quirks mode and therefore layout.
            _ => Err(TokenizerError::DoctypeBranchUnsupported {
                offset: self.position,
            }),
        }
    }

    fn emit_doctype(&mut self, name: Option<String>, public_id: Option<String>) {
        self.flush_characters();
        self.tokens.push(Token::Doctype {
            name,
            public_id,
            system_id: None,
            force_quirks: self.doctype_force_quirks,
        });
        self.state = State::Data;
    }

    fn step_bogus_comment(&mut self, byte: u8) {
        if byte == b'>' {
            let comment = core::mem::take(&mut self.comment);
            self.flush_characters();
            self.tokens.push(Token::Comment(comment));
            self.state = State::Data;
            self.position += 1;
        } else {
            self.comment.push(byte as char);
            self.position += 1;
        }
    }

    // -- character references --------------------------------------------

    fn consume_character_reference(&mut self) {
        let resolved = self.take_character_reference();
        self.pending_characters.push_str(&resolved);
    }

    /// Resolves a character reference at the current position.
    ///
    /// Covers numeric references and the named references that appear in
    /// ordinary markup. An unrecognized reference is returned literally, which
    /// is what the specification requires: `&notareference;` is text.
    fn take_character_reference(&mut self) -> String {
        let start = self.position;
        debug_assert_eq!(self.input[start], b'&');
        let rest = &self.input[start + 1..];

        if let Some(&b'#') = rest.first() {
            return self.take_numeric_reference(start);
        }

        let name_len = rest
            .iter()
            .take_while(|byte| byte.is_ascii_alphanumeric())
            .count();
        if name_len == 0 || rest.get(name_len) != Some(&b';') {
            self.position = start + 1;
            return "&".to_string();
        }
        let name = core::str::from_utf8(&rest[..name_len]).unwrap_or_default();
        match named_reference(name) {
            Some(resolved) => {
                self.position = start + 1 + name_len + 1;
                resolved.to_string()
            }
            None => {
                self.position = start + 1;
                "&".to_string()
            }
        }
    }

    fn take_numeric_reference(&mut self, start: usize) -> String {
        let after_hash = start + 2;
        let (radix, digits_start) = match self.input.get(after_hash) {
            Some(b'x' | b'X') => (16, after_hash + 1),
            _ => (10, after_hash),
        };
        let digit_len = self.input[digits_start..]
            .iter()
            .take_while(|byte| byte.is_ascii_hexdigit())
            .count();
        if digit_len == 0 {
            self.error(ParseErrorKind::MalformedCharacterReference);
            self.position = start + 1;
            return "&".to_string();
        }
        let digits =
            core::str::from_utf8(&self.input[digits_start..digits_start + digit_len]).unwrap_or("");
        let mut end = digits_start + digit_len;
        if self.input.get(end) == Some(&b';') {
            end += 1;
        } else {
            self.error(ParseErrorKind::MalformedCharacterReference);
        }
        self.position = end;
        u32::from_str_radix(digits, radix)
            .ok()
            .and_then(char::from_u32)
            // U+FFFD is the specified replacement for unpaired surrogates and
            // out-of-range scalar values.
            .map_or_else(|| "\u{FFFD}".to_string(), |value| value.to_string())
    }

    // -- shared ----------------------------------------------------------

    fn flush_characters(&mut self) {
        if self.pending_characters.is_empty() {
            return;
        }
        let text = core::mem::take(&mut self.pending_characters);
        self.tokens.push(Token::Characters(text));
    }

    fn error(&mut self, kind: ParseErrorKind) {
        self.errors.push(ParseError {
            offset: self.position,
            kind,
        });
    }

    fn finish_at_eof(&mut self) {
        match self.state {
            State::TagOpen
            | State::EndTagOpen
            | State::TagName
            | State::BeforeAttributeName
            | State::AttributeName
            | State::AfterAttributeName
            | State::BeforeAttributeValue
            | State::AttributeValueDoubleQuoted
            | State::AttributeValueSingleQuoted
            | State::AttributeValueUnquoted
            | State::AfterAttributeValueQuoted
            | State::SelfClosingStartTag => self.error(ParseErrorKind::EofInTag),
            State::CommentStart | State::Comment | State::CommentEndDash | State::CommentEnd => {
                self.error(ParseErrorKind::EofInComment);
            }
            State::Doctype | State::DoctypeName | State::AfterDoctypeName => {
                self.error(ParseErrorKind::EofInDoctype);
            }
            State::Data | State::RawTextLike | State::MarkupDeclarationOpen => {}
            State::BogusComment => {
                let comment = core::mem::take(&mut self.comment);
                self.tokens.push(Token::Comment(comment));
            }
        }
    }
}

/// Returns the content model an element switches the tokenizer into, if any.
fn raw_text_model_for(tag_name: &str) -> Option<ContentModel> {
    match tag_name {
        "script" => Some(ContentModel::ScriptData),
        "style" | "xmp" | "iframe" | "noembed" | "noframes" => Some(ContentModel::RawText),
        "title" | "textarea" => Some(ContentModel::RcData),
        _ => None,
    }
}

/// Resolves the named character references reachable from ordinary markup.
///
/// The full WHATWG table has over two thousand entries and is a build-time
/// artifact in mature engines. This subset covers the references that appear
/// in practice; anything absent is returned literally rather than guessed.
fn named_reference(name: &str) -> Option<&'static str> {
    Some(match name {
        "amp" => "&",
        "lt" => "<",
        "gt" => ">",
        "quot" => "\"",
        "apos" => "'",
        "nbsp" => "\u{A0}",
        "copy" => "\u{A9}",
        "reg" => "\u{AE}",
        "trade" => "\u{2122}",
        "hellip" => "\u{2026}",
        "mdash" => "\u{2014}",
        "ndash" => "\u{2013}",
        "lsquo" => "\u{2018}",
        "rsquo" => "\u{2019}",
        "ldquo" => "\u{201C}",
        "rdquo" => "\u{201D}",
        "middot" => "\u{B7}",
        "bull" => "\u{2022}",
        "deg" => "\u{B0}",
        "plusmn" => "\u{B1}",
        "times" => "\u{D7}",
        "divide" => "\u{F7}",
        "euro" => "\u{20AC}",
        "pound" => "\u{A3}",
        "yen" => "\u{A5}",
        "cent" => "\u{A2}",
        "sect" => "\u{A7}",
        "para" => "\u{B6}",
        "dagger" => "\u{2020}",
        "laquo" => "\u{AB}",
        "raquo" => "\u{BB}",
        _ => return None,
    })
}

/// Returns the length in bytes of the UTF-8 sequence starting with `first`.
const fn utf8_sequence_length(first: u8) -> usize {
    if first < 0x80 {
        1
    } else if first >> 5 == 0b110 {
        2
    } else if first >> 4 == 0b1110 {
        3
    } else if first >> 3 == 0b11110 {
        4
    } else {
        // A continuation byte here means the input was not valid UTF-8.
        // Advancing by one keeps the tokenizer making progress.
        1
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn tokens(input: &str) -> Vec<Token> {
        Tokenizer::new(input).tokenize().expect("tokenizes").tokens
    }

    fn start(name: &str, attributes: &[(&str, &str)], self_closing: bool) -> Token {
        Token::StartTag {
            name: name.to_string(),
            attributes: attributes
                .iter()
                .map(|(key, value)| Attribute {
                    name: (*key).to_string(),
                    value: (*value).to_string(),
                })
                .collect(),
            self_closing,
        }
    }

    #[test]
    fn tokenizes_text_only_input() {
        assert_eq!(
            tokens("hello world"),
            vec![Token::Characters("hello world".to_string())]
        );
    }

    #[test]
    fn tokenizes_simple_element() {
        assert_eq!(
            tokens("<p>hi</p>"),
            vec![
                start("p", &[], false),
                Token::Characters("hi".to_string()),
                Token::EndTag {
                    name: "p".to_string()
                },
            ]
        );
    }

    #[test]
    fn lowercases_tag_and_attribute_names() {
        assert_eq!(
            tokens("<DIV CLASS=\"a\">"),
            vec![start("div", &[("class", "a")], false)]
        );
    }

    #[test]
    fn handles_all_three_attribute_quoting_forms() {
        assert_eq!(
            tokens("<a href=\"x\" id='y' rel=z>"),
            vec![start(
                "a",
                &[("href", "x"), ("id", "y"), ("rel", "z")],
                false
            )]
        );
    }

    #[test]
    fn handles_valueless_attributes() {
        assert_eq!(
            tokens("<input disabled hidden>"),
            vec![start("input", &[("disabled", ""), ("hidden", "")], false)]
        );
    }

    #[test]
    fn records_self_closing_flag() {
        assert_eq!(tokens("<br/>"), vec![start("br", &[], true)]);
    }

    #[test]
    fn tokenizes_comments() {
        assert_eq!(
            tokens("<!-- note -->"),
            vec![Token::Comment(" note ".to_string())]
        );
    }

    #[test]
    fn comment_containing_dashes_terminates_correctly() {
        assert_eq!(
            tokens("<!-- a--b -->"),
            vec![Token::Comment(" a--b ".to_string())]
        );
    }

    #[test]
    fn tokenizes_doctype() {
        assert_eq!(
            tokens("<!DOCTYPE html>"),
            vec![Token::Doctype {
                name: Some("html".to_string()),
                public_id: None,
                system_id: None,
                force_quirks: false,
            }]
        );
    }

    #[test]
    fn resolves_named_and_numeric_character_references() {
        assert_eq!(
            tokens("&amp;&#65;&#x42;&nbsp;"),
            vec![Token::Characters("&AB\u{A0}".to_string())]
        );
    }

    #[test]
    fn leaves_unknown_character_reference_literal() {
        assert_eq!(
            tokens("&notareference;"),
            vec![Token::Characters("&notareference;".to_string())]
        );
    }

    #[test]
    fn resolves_character_references_inside_attribute_values() {
        assert_eq!(
            tokens("<a title=\"a&amp;b\">"),
            vec![start("a", &[("title", "a&b")], false)]
        );
    }

    #[test]
    fn script_contents_are_not_tokenized_as_markup() {
        // The `<b>` inside the script is character data, not a start tag.
        // Getting this wrong is a classic source of injection bugs.
        assert_eq!(
            tokens("<script>var a = \"<b>\";</script>"),
            vec![
                start("script", &[], false),
                Token::Characters("var a = \"<b>\";".to_string()),
                Token::EndTag {
                    name: "script".to_string()
                },
            ]
        );
    }

    #[test]
    fn style_contents_are_raw_text() {
        assert_eq!(
            tokens("<style>a{content:\"<x>\"}</style>"),
            vec![
                start("style", &[], false),
                Token::Characters("a{content:\"<x>\"}".to_string()),
                Token::EndTag {
                    name: "style".to_string()
                },
            ]
        );
    }

    #[test]
    fn rcdata_resolves_references_but_not_tags() {
        assert_eq!(
            tokens("<title>a&amp;b <x></title>"),
            vec![
                start("title", &[], false),
                Token::Characters("a&b <x>".to_string()),
                Token::EndTag {
                    name: "title".to_string()
                },
            ]
        );
    }

    #[test]
    fn self_closing_script_does_not_enter_raw_text() {
        assert_eq!(
            tokens("<script/><p>"),
            vec![start("script", &[], true), start("p", &[], false)]
        );
    }

    #[test]
    fn duplicate_attribute_is_reported_and_dropped() {
        let result = Tokenizer::new("<a id=\"one\" id=\"two\">")
            .tokenize()
            .expect("tokenizes");
        assert_eq!(result.tokens, vec![start("a", &[("id", "one")], false)]);
        assert_eq!(result.errors.len(), 1);
        assert_eq!(result.errors[0].kind, ParseErrorKind::DuplicateAttribute);
    }

    #[test]
    fn unterminated_tag_reports_eof_error() {
        let result = Tokenizer::new("<div class=").tokenize().expect("tokenizes");
        assert_eq!(result.errors.len(), 1);
        assert_eq!(result.errors[0].kind, ParseErrorKind::EofInTag);
    }

    #[test]
    fn stray_less_than_is_text() {
        let result = Tokenizer::new("a < b").tokenize().expect("tokenizes");
        assert_eq!(result.tokens, vec![Token::Characters("a < b".to_string())]);
        assert_eq!(
            result.errors[0].kind,
            ParseErrorKind::InvalidFirstCharacterOfTagName
        );
    }

    #[test]
    fn multibyte_text_survives_tokenization() {
        assert_eq!(
            tokens("<p>héllo — 世界</p>"),
            vec![
                start("p", &[], false),
                Token::Characters("héllo — 世界".to_string()),
                Token::EndTag {
                    name: "p".to_string()
                },
            ]
        );
    }

    #[test]
    fn cdata_section_is_reported_not_guessed() {
        let error = Tokenizer::new("<![CDATA[x]]>")
            .tokenize()
            .expect_err("CDATA is unsupported");
        assert!(matches!(
            error,
            TokenizerError::CdataSectionUnsupported { .. }
        ));
    }

    #[test]
    fn doctype_with_public_identifier_is_reported_not_guessed() {
        let error = Tokenizer::new("<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.01//EN\">")
            .tokenize()
            .expect_err("DOCTYPE branch is unsupported");
        assert!(matches!(
            error,
            TokenizerError::DoctypeBranchUnsupported { .. }
        ));
    }

    #[test]
    fn tokenizes_a_small_document() {
        let html = "<!DOCTYPE html><html><head><title>T</title></head>\
                    <body><h1 class=\"a\">Hi</h1><!-- c --><p>x&amp;y</p></body></html>";
        let result = Tokenizer::new(html).tokenize().expect("tokenizes");
        assert!(result.errors.is_empty(), "unexpected: {:?}", result.errors);
        assert_eq!(
            result.tokens.first(),
            Some(&Token::Doctype {
                name: Some("html".to_string()),
                public_id: None,
                system_id: None,
                force_quirks: false,
            })
        );
        assert!(
            result
                .tokens
                .contains(&Token::Characters("x&y".to_string()))
        );
    }
}
