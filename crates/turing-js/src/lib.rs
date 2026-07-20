// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! Turing-owned ECMAScript frontend and bytecode interpreter.
//!
//! This crate implements `WP-010` and `REQ-JS-001`: a lexer, a parser, a
//! bytecode compiler, and a stack virtual machine. It is written from the
//! ECMAScript specification and derives from no existing engine, consistent
//! with `ADR-0009` Option A and with `ADR-0004`, which keeps the JavaScript
//! runtime Turing-owned.
//!
//! # Why bytecode rather than a tree walker
//!
//! A tree-walking interpreter is simpler, but the shape of the eventual engine
//! matters more than the shortest path to running code. Compiling to a flat
//! instruction stream separates parsing cost from execution cost, gives a
//! stable surface for the baseline JIT that `WP-019` describes, and makes
//! scope resolution a compile-time concern rather than a runtime hash lookup.
//! Choosing this now avoids a rewrite later.
//!
//! # Deliberate limits
//!
//! Implemented: numbers, strings, booleans, `null`, `undefined`, `var`/`let`/
//! `const` bindings, arithmetic and comparison, logical operators with
//! short-circuit evaluation, `if`/`else`, `while`, blocks with lexical
//! scoping, function declarations, calls, recursion, and `return`.
//!
//! Everything else returns a typed error rather than a partial evaluation:
//! objects and property access, arrays, closures over enclosing scope,
//! `class`, `try`/`catch`, `async`/`await`, generators, regular expressions,
//! modules, `eval`, and prototype semantics.
//!
//! The reason is sharper here than elsewhere in the engine. A partially
//! implemented language does not fail visibly; it computes a wrong value and
//! carries on. Refusing an unimplemented construct at compile time keeps every
//! program that *does* run trustworthy.

#![forbid(unsafe_code)]

use core::fmt;
use turing_gc::{Bindings, GcRef, Heap, Trace};

/// A construct this implementation does not model, or a program error.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum JsError {
    /// The lexer met a character it cannot start a token with.
    UnexpectedCharacter { character: char, offset: usize },
    /// The parser met a token it cannot use here.
    UnexpectedToken { found: String, expected: String },
    /// The source nests deeper than the parser will recurse.
    NestingTooDeep { limit: usize },
    /// A language feature that is not implemented.
    Unsupported { feature: String },
    /// A name was used before it was declared.
    UndefinedVariable { name: String },
    /// Assignment to a `const` binding.
    AssignmentToConstant { name: String },
    /// A runtime type error, such as calling a non-function.
    TypeError { message: String },
    /// Execution exceeded the instruction budget.
    StepLimitExceeded { limit: u64 },
    /// Execution produced more string data than the byte budget allows.
    ByteLimitExceeded { limit: u64 },
    /// A name was called that is neither a script function nor a bound
    /// operation.
    UnboundOperation { name: String },
    /// A bound operation was called with the wrong number of arguments.
    OperationArity {
        name: String,
        expected: usize,
        got: usize,
    },
    /// A bound operation refused or failed.
    HostOperationFailed { name: String, message: String },
}

impl fmt::Display for JsError {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::UnexpectedCharacter { character, offset } => {
                write!(
                    formatter,
                    "unexpected character {character:?} at byte {offset}"
                )
            }
            Self::NestingTooDeep { limit } => write!(
                formatter,
                "the source nests deeper than {limit} levels; the parser is                  recursive descent, and continuing would overflow the stack,                  which aborts the process rather than returning an error"
            ),
            Self::UnexpectedToken { found, expected } => {
                write!(formatter, "unexpected {found}; expected {expected}")
            }
            Self::Unsupported { feature } => write!(
                formatter,
                "{feature} is not implemented; refusing rather than evaluating it partially"
            ),
            Self::UndefinedVariable { name } => write!(formatter, "{name} is not defined"),
            Self::AssignmentToConstant { name } => {
                write!(formatter, "assignment to constant {name}")
            }
            Self::TypeError { message } => write!(formatter, "TypeError: {message}"),
            Self::UnboundOperation { name } => write!(
                formatter,
                "{name} is neither a declared function nor a bound operation; \
                 treating an unknown call as no-op or `undefined` would turn a \
                 typo into silence"
            ),
            Self::OperationArity {
                name,
                expected,
                got,
            } => write!(
                formatter,
                "{name} is bound with {expected} parameter(s) and was called with \
                 {got}; the registry records arity, so a mismatch is a declared \
                 contract being broken rather than a convention"
            ),
            Self::HostOperationFailed { name, message } => {
                write!(formatter, "the bound operation {name} failed: {message}")
            }
            Self::ByteLimitExceeded { limit } => write!(
                formatter,
                "execution produced more than {limit} bytes of string data; a step \
                 limit bounds how many operations run, not how much each one \
                 allocates, and repeated concatenation doubles its result every step"
            ),
            Self::StepLimitExceeded { limit } => {
                write!(formatter, "execution exceeded {limit} instructions")
            }
        }
    }
}

// -- values --------------------------------------------------------------

/// A runtime value.
#[derive(Clone, Debug, PartialEq)]
pub enum Value {
    Undefined,
    Null,
    Boolean(bool),
    Number(f64),
    String(String),
    /// Index into the compiled function table.
    Function(usize),
    /// A reference into the collected heap.
    ///
    /// A handle rather than the object itself, because `o.self = o` is
    /// expressible and an owned representation would not terminate. The
    /// reference carries a generation, so using one after its object was
    /// collected is refused rather than silently reading whatever now occupies
    /// the slot.
    Object(GcRef),
}

impl Value {
    /// Applies the specification's `ToBoolean`.
    #[must_use]
    pub fn truthy(&self) -> bool {
        match self {
            Self::Undefined | Self::Null => false,
            Self::Boolean(value) => *value,
            // NaN and both zeroes are falsy; this is easy to get wrong.
            Self::Number(value) => *value != 0.0 && !value.is_nan(),
            Self::String(value) => !value.is_empty(),
            // Every object is truthy, including an empty one. This is the case
            // people expect to behave like an empty string and it does not.
            Self::Function(_) | Self::Object(_) => true,
        }
    }
}

impl fmt::Display for Value {
    fn fmt(&self, formatter: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Undefined => write!(formatter, "undefined"),
            Self::Null => write!(formatter, "null"),
            Self::Boolean(value) => write!(formatter, "{value}"),
            Self::Number(value) => {
                if value.fract() == 0.0 && value.is_finite() {
                    write!(formatter, "{}", *value as i64)
                } else {
                    write!(formatter, "{value}")
                }
            }
            Self::String(value) => write!(formatter, "{value}"),
            Self::Function(index) => write!(formatter, "[function {index}]"),
            // Deliberately not the object's contents. Rendering them would need
            // cycle detection, and `String(o)` in the language is "[object
            // Object]" rather than a dump.
            Self::Object(_) => write!(formatter, "[object Object]"),
        }
    }
}

// -- lexer ---------------------------------------------------------------

#[derive(Clone, Debug, Eq, PartialEq)]
enum Token {
    Number(String),
    Str(String),
    Ident(String),
    Keyword(String),
    Punct(String),
    Eof,
}

impl Token {
    fn describe(&self) -> String {
        match self {
            Self::Number(text)
            | Self::Str(text)
            | Self::Ident(text)
            | Self::Keyword(text)
            | Self::Punct(text) => format!("`{text}`"),
            Self::Eof => "end of input".to_string(),
        }
    }
}

const KEYWORDS: &[&str] = &[
    "var",
    "let",
    "const",
    "if",
    "else",
    "while",
    "function",
    "return",
    "true",
    "false",
    "null",
    "undefined",
    "class",
    "try",
    "catch",
    "finally",
    "throw",
    "async",
    "await",
    "function*",
    "yield",
    "new",
    "delete",
    "typeof",
    "instanceof",
    "for",
    "do",
    "switch",
    "import",
    "export",
];

/// Keywords that name a feature this implementation refuses outright.
const REFUSED_KEYWORDS: &[(&str, &str)] = &[
    ("class", "class"),
    ("try", "try/catch"),
    ("catch", "try/catch"),
    ("finally", "try/catch"),
    ("throw", "throw"),
    ("async", "async functions"),
    ("await", "await"),
    ("yield", "generators"),
    ("new", "constructors"),
    ("delete", "delete"),
    ("instanceof", "instanceof"),
    ("switch", "switch"),
    ("import", "modules"),
    ("export", "modules"),
    ("for", "for loops"),
    ("do", "do/while"),
];

fn lex(source: &str) -> Result<Vec<Token>, JsError> {
    let bytes = source.as_bytes();
    let mut tokens = Vec::new();
    let mut index = 0;

    while index < bytes.len() {
        let byte = bytes[index];
        if byte.is_ascii_whitespace() {
            index += 1;
            continue;
        }
        // Line comments.
        if bytes[index..].starts_with(b"//") {
            while index < bytes.len() && bytes[index] != b'\n' {
                index += 1;
            }
            continue;
        }
        if bytes[index..].starts_with(b"/*") {
            index += 2;
            while index < bytes.len() && !bytes[index..].starts_with(b"*/") {
                index += 1;
            }
            index = (index + 2).min(bytes.len());
            continue;
        }
        if byte.is_ascii_digit() {
            let start = index;
            while index < bytes.len() && (bytes[index].is_ascii_digit() || bytes[index] == b'.') {
                index += 1;
            }
            tokens.push(Token::Number(source[start..index].to_string()));
            continue;
        }
        if byte == b'"' || byte == b'\'' {
            let quote = byte;
            index += 1;
            let start = index;
            while index < bytes.len() && bytes[index] != quote {
                index += 1;
            }
            tokens.push(Token::Str(source[start..index].to_string()));
            index += 1;
            continue;
        }
        if byte.is_ascii_alphabetic() || byte == b'_' || byte == b'$' {
            let start = index;
            while index < bytes.len()
                && (bytes[index].is_ascii_alphanumeric()
                    || bytes[index] == b'_'
                    || bytes[index] == b'$')
            {
                index += 1;
            }
            let word = &source[start..index];
            if KEYWORDS.contains(&word) {
                tokens.push(Token::Keyword(word.to_string()));
            } else {
                tokens.push(Token::Ident(word.to_string()));
            }
            continue;
        }
        // Multi-character operators are matched longest-first so that `===`
        // does not lex as `==` followed by `=`.
        let three = source.get(index..index + 3).unwrap_or("");
        let two = source.get(index..index + 2).unwrap_or("");
        if matches!(three, "===" | "!==") {
            tokens.push(Token::Punct(three.to_string()));
            index += 3;
            continue;
        }
        // `...` before `.`, so spread lexes as one token and can be refused
        // as itself rather than as three property accesses.
        if three == "..." {
            tokens.push(Token::Punct(three.to_string()));
            index += 3;
            continue;
        }
        if matches!(two, "==" | "!=" | "<=" | ">=" | "&&" | "||") {
            tokens.push(Token::Punct(two.to_string()));
            index += 2;
            continue;
        }
        if b"+-*/%<>=!(){};,.[]:?".contains(&byte) {
            tokens.push(Token::Punct((byte as char).to_string()));
            index += 1;
            continue;
        }
        // Regular expressions and template literals begin here.
        return Err(JsError::UnexpectedCharacter {
            character: byte as char,
            offset: index,
        });
    }
    tokens.push(Token::Eof);
    Ok(tokens)
}

// -- ast -----------------------------------------------------------------

#[derive(Clone, Debug, PartialEq)]
enum Expr {
    Number(f64),
    Str(String),
    Boolean(bool),
    Null,
    Undefined,
    Variable(String),
    Unary {
        operator: String,
        operand: Box<Expr>,
    },
    Binary {
        operator: String,
        left: Box<Expr>,
        right: Box<Expr>,
    },
    Logical {
        operator: String,
        left: Box<Expr>,
        right: Box<Expr>,
    },
    Assign {
        name: String,
        value: Box<Expr>,
    },
    Call {
        callee: String,
        arguments: Vec<Expr>,
    },
    /// `{ a: 1, "b": 2 }`, in source order.
    ObjectLiteral {
        entries: Vec<(String, Expr)>,
    },
    /// `object.name` or `object[key]`.
    Member {
        object: Box<Expr>,
        key: Box<Expr>,
    },
    /// `object.name = value` or `object[key] = value`.
    SetMember {
        object: Box<Expr>,
        key: Box<Expr>,
        value: Box<Expr>,
    },
}

#[derive(Clone, Debug, PartialEq)]
enum Stmt {
    Declare {
        name: String,
        value: Option<Expr>,
        constant: bool,
    },
    Expression(Expr),
    Block(Vec<Stmt>),
    If {
        condition: Expr,
        then_branch: Box<Stmt>,
        else_branch: Option<Box<Stmt>>,
    },
    While {
        condition: Expr,
        body: Box<Stmt>,
    },
    Function {
        name: String,
        parameters: Vec<String>,
        body: Vec<Stmt>,
    },
    Return(Option<Expr>),
}

// -- parser --------------------------------------------------------------

/// The deepest grammatical nesting the parser will descend through.
///
/// This is a recursive-descent parser, so nesting in the source becomes
/// recursion on the native stack. A stack overflow aborts the process and
/// cannot be caught, so depth is bounded here rather than left to chance.
/// `((((1))))`, `if(1){if(1){…}}`, and `-----1` all reach it, and all three are
/// trivially producible by a hostile page.
///
/// # Where the number comes from
///
/// Measured, not chosen. With the bound removed, parsing overflowed a 1 MiB
/// stack at roughly 95 nested parentheses in a debug build. The precedence
/// chain runs about ten frames per expression level, which is why the figure is
/// that low.
///
/// Each source nesting level costs about two counted levels here, so this bound
/// stops at roughly thirty source levels — about a third of the measured
/// failure point. The margin is deliberately generous because the true limit
/// varies with stack size, platform, and build profile, and the cost of being
/// wrong is an uncatchable abort rather than a recoverable error.
///
/// Still far above real programs: expressions nest single digits deep in
/// practice, and deeply parenthesised source is a pathological pattern rather
/// than something a person or a minifier produces.
pub const MAX_NESTING_DEPTH: usize = 64;

struct Parser {
    tokens: Vec<Token>,
    position: usize,
    /// Current recursion depth, bounded by [`MAX_NESTING_DEPTH`].
    depth: usize,
}

impl Parser {
    const fn new(tokens: Vec<Token>) -> Self {
        Self {
            tokens,
            position: 0,
            depth: 0,
        }
    }

    /// Enters one level of grammatical nesting.
    ///
    /// Paired with [`Self::leave`]. Every production that can recurse into
    /// itself calls this first, so one check covers expressions, statements,
    /// and blocks alike rather than each growing its own counter.
    fn enter(&mut self) -> Result<(), JsError> {
        self.depth += 1;
        if self.depth > MAX_NESTING_DEPTH {
            return Err(JsError::NestingTooDeep {
                limit: MAX_NESTING_DEPTH,
            });
        }
        Ok(())
    }

    fn leave(&mut self) {
        self.depth -= 1;
    }

    fn peek(&self) -> &Token {
        self.tokens.get(self.position).unwrap_or(&Token::Eof)
    }

    fn advance(&mut self) -> Token {
        let token = self.peek().clone();
        self.position += 1;
        token
    }

    fn check_punct(&self, text: &str) -> bool {
        matches!(self.peek(), Token::Punct(value) if value == text)
    }

    fn check_keyword(&self, text: &str) -> bool {
        matches!(self.peek(), Token::Keyword(value) if value == text)
    }

    fn eat_punct(&mut self, text: &str) -> bool {
        if self.check_punct(text) {
            self.position += 1;
            true
        } else {
            false
        }
    }

    fn expect_punct(&mut self, text: &str) -> Result<(), JsError> {
        if self.eat_punct(text) {
            Ok(())
        } else {
            Err(JsError::UnexpectedToken {
                found: self.peek().describe(),
                expected: format!("`{text}`"),
            })
        }
    }

    fn refuse_unsupported_keyword(&self) -> Result<(), JsError> {
        if let Token::Keyword(word) = self.peek()
            && let Some((_, feature)) = REFUSED_KEYWORDS.iter().find(|(k, _)| k == word)
        {
            return Err(JsError::Unsupported {
                feature: (*feature).to_string(),
            });
        }
        Ok(())
    }

    fn parse_program(&mut self) -> Result<Vec<Stmt>, JsError> {
        let mut statements = Vec::new();
        while !matches!(self.peek(), Token::Eof) {
            statements.push(self.parse_statement()?);
        }
        Ok(statements)
    }

    fn parse_statement(&mut self) -> Result<Stmt, JsError> {
        self.enter()?;
        let statement = self.parse_statement_inner();
        self.leave();
        statement
    }

    fn parse_statement_inner(&mut self) -> Result<Stmt, JsError> {
        self.refuse_unsupported_keyword()?;

        if self.check_keyword("function") {
            return self.parse_function();
        }
        if self.check_keyword("var") || self.check_keyword("let") || self.check_keyword("const") {
            let Token::Keyword(kind) = self.advance() else {
                unreachable!("checked above")
            };
            let Token::Ident(name) = self.advance() else {
                return Err(JsError::UnexpectedToken {
                    found: "token".to_string(),
                    expected: "a binding name".to_string(),
                });
            };
            let value = if self.eat_punct("=") {
                Some(self.parse_expression()?)
            } else {
                None
            };
            self.eat_punct(";");
            return Ok(Stmt::Declare {
                name,
                value,
                constant: kind == "const",
            });
        }
        if self.check_keyword("if") {
            self.position += 1;
            self.expect_punct("(")?;
            let condition = self.parse_expression()?;
            self.expect_punct(")")?;
            let then_branch = Box::new(self.parse_statement()?);
            let else_branch = if self.check_keyword("else") {
                self.position += 1;
                Some(Box::new(self.parse_statement()?))
            } else {
                None
            };
            return Ok(Stmt::If {
                condition,
                then_branch,
                else_branch,
            });
        }
        if self.check_keyword("while") {
            self.position += 1;
            self.expect_punct("(")?;
            let condition = self.parse_expression()?;
            self.expect_punct(")")?;
            let body = Box::new(self.parse_statement()?);
            return Ok(Stmt::While { condition, body });
        }
        if self.check_keyword("return") {
            self.position += 1;
            let value = if self.check_punct(";") || self.check_punct("}") {
                None
            } else {
                Some(self.parse_expression()?)
            };
            self.eat_punct(";");
            return Ok(Stmt::Return(value));
        }
        if self.eat_punct("{") {
            let mut statements = Vec::new();
            while !self.check_punct("}") && !matches!(self.peek(), Token::Eof) {
                statements.push(self.parse_statement()?);
            }
            self.expect_punct("}")?;
            return Ok(Stmt::Block(statements));
        }

        let expression = self.parse_expression()?;
        self.eat_punct(";");
        Ok(Stmt::Expression(expression))
    }

    fn parse_function(&mut self) -> Result<Stmt, JsError> {
        self.position += 1; // `function`
        let Token::Ident(name) = self.advance() else {
            return Err(JsError::UnexpectedToken {
                found: "token".to_string(),
                expected: "a function name".to_string(),
            });
        };
        self.expect_punct("(")?;
        let mut parameters = Vec::new();
        while !self.check_punct(")") {
            let Token::Ident(parameter) = self.advance() else {
                return Err(JsError::UnexpectedToken {
                    found: "token".to_string(),
                    expected: "a parameter name".to_string(),
                });
            };
            parameters.push(parameter);
            if !self.eat_punct(",") {
                break;
            }
        }
        self.expect_punct(")")?;
        self.expect_punct("{")?;
        let mut body = Vec::new();
        while !self.check_punct("}") && !matches!(self.peek(), Token::Eof) {
            body.push(self.parse_statement()?);
        }
        self.expect_punct("}")?;
        Ok(Stmt::Function {
            name,
            parameters,
            body,
        })
    }

    fn parse_expression(&mut self) -> Result<Expr, JsError> {
        self.enter()?;
        let expression = self.parse_assignment();
        self.leave();
        expression
    }

    fn parse_assignment(&mut self) -> Result<Expr, JsError> {
        let target = self.parse_logical_or()?;
        if self.check_punct("=") {
            self.position += 1;
            let value = Box::new(self.parse_assignment()?);
            return match target {
                Expr::Variable(name) => Ok(Expr::Assign { name, value }),
                Expr::Member { object, key } => Ok(Expr::SetMember { object, key, value }),
                _ => Err(JsError::UnexpectedToken {
                    found: "expression".to_string(),
                    expected: "a variable or property on the left of `=`".to_string(),
                }),
            };
        }
        Ok(target)
    }

    fn parse_logical_or(&mut self) -> Result<Expr, JsError> {
        let mut left = self.parse_logical_and()?;
        while self.check_punct("||") {
            self.position += 1;
            let right = Box::new(self.parse_logical_and()?);
            left = Expr::Logical {
                operator: "||".to_string(),
                left: Box::new(left),
                right,
            };
        }
        Ok(left)
    }

    fn parse_logical_and(&mut self) -> Result<Expr, JsError> {
        let mut left = self.parse_equality()?;
        while self.check_punct("&&") {
            self.position += 1;
            let right = Box::new(self.parse_equality()?);
            left = Expr::Logical {
                operator: "&&".to_string(),
                left: Box::new(left),
                right,
            };
        }
        Ok(left)
    }

    fn parse_equality(&mut self) -> Result<Expr, JsError> {
        let mut left = self.parse_comparison()?;
        loop {
            let operator = match self.peek() {
                Token::Punct(value) if matches!(value.as_str(), "==" | "!=" | "===" | "!==") => {
                    value.clone()
                }
                _ => break,
            };
            self.position += 1;
            let right = Box::new(self.parse_comparison()?);
            left = Expr::Binary {
                operator,
                left: Box::new(left),
                right,
            };
        }
        Ok(left)
    }

    fn parse_comparison(&mut self) -> Result<Expr, JsError> {
        let mut left = self.parse_additive()?;
        loop {
            let operator = match self.peek() {
                Token::Punct(value) if matches!(value.as_str(), "<" | ">" | "<=" | ">=") => {
                    value.clone()
                }
                _ => break,
            };
            self.position += 1;
            let right = Box::new(self.parse_additive()?);
            left = Expr::Binary {
                operator,
                left: Box::new(left),
                right,
            };
        }
        Ok(left)
    }

    fn parse_additive(&mut self) -> Result<Expr, JsError> {
        let mut left = self.parse_multiplicative()?;
        loop {
            let operator = match self.peek() {
                Token::Punct(value) if matches!(value.as_str(), "+" | "-") => value.clone(),
                _ => break,
            };
            self.position += 1;
            let right = Box::new(self.parse_multiplicative()?);
            left = Expr::Binary {
                operator,
                left: Box::new(left),
                right,
            };
        }
        Ok(left)
    }

    fn parse_multiplicative(&mut self) -> Result<Expr, JsError> {
        let mut left = self.parse_unary()?;
        loop {
            let operator = match self.peek() {
                Token::Punct(value) if matches!(value.as_str(), "*" | "/" | "%") => value.clone(),
                _ => break,
            };
            self.position += 1;
            let right = Box::new(self.parse_unary()?);
            left = Expr::Binary {
                operator,
                left: Box::new(left),
                right,
            };
        }
        Ok(left)
    }

    fn parse_unary(&mut self) -> Result<Expr, JsError> {
        self.enter()?;
        let expression = self.parse_unary_inner();
        self.leave();
        expression
    }

    fn parse_unary_inner(&mut self) -> Result<Expr, JsError> {
        if let Token::Punct(value) = self.peek()
            && matches!(value.as_str(), "-" | "!")
        {
            let operator = value.clone();
            self.position += 1;
            let operand = Box::new(self.parse_unary()?);
            return Ok(Expr::Unary { operator, operand });
        }
        if self.check_keyword("typeof") {
            return Err(JsError::Unsupported {
                feature: "typeof".to_string(),
            });
        }
        self.parse_primary()
    }

    fn parse_primary(&mut self) -> Result<Expr, JsError> {
        let primary = self.parse_primary_base()?;
        self.parse_member_suffix(primary)
    }

    /// Consumes any run of `.name` and `[key]` suffixes.
    ///
    /// A loop rather than recursion into `parse_primary`, so `a.b.c` costs one
    /// level of grammatical nesting rather than three.
    fn parse_member_suffix(&mut self, mut object: Expr) -> Result<Expr, JsError> {
        loop {
            if self.eat_punct(".") {
                let Token::Ident(name) = self.advance() else {
                    return Err(JsError::UnexpectedToken {
                        found: "token".to_string(),
                        expected: "a property name after `.`".to_string(),
                    });
                };
                object = Expr::Member {
                    object: Box::new(object),
                    key: Box::new(Expr::Str(name)),
                };
            } else if self.eat_punct("[") {
                let key = self.parse_expression()?;
                self.expect_punct("]")?;
                object = Expr::Member {
                    object: Box::new(object),
                    key: Box::new(key),
                };
            } else {
                return Ok(object);
            }
        }
    }

    fn parse_primary_base(&mut self) -> Result<Expr, JsError> {
        self.refuse_unsupported_keyword()?;
        if self.check_punct("{") {
            return self.parse_object_literal();
        }
        match self.advance() {
            Token::Number(text) => Ok(Expr::Number(text.parse::<f64>().unwrap_or(f64::NAN))),
            Token::Str(text) => Ok(Expr::Str(text)),
            Token::Keyword(word) => match word.as_str() {
                "true" => Ok(Expr::Boolean(true)),
                "false" => Ok(Expr::Boolean(false)),
                "null" => Ok(Expr::Null),
                "undefined" => Ok(Expr::Undefined),
                "function" => Err(JsError::Unsupported {
                    feature: "function expressions and closures".to_string(),
                }),
                other => Err(JsError::Unsupported {
                    feature: other.to_string(),
                }),
            },
            Token::Ident(name) => {
                if self.eat_punct("(") {
                    let mut arguments = Vec::new();
                    while !self.check_punct(")") {
                        arguments.push(self.parse_expression()?);
                        if !self.eat_punct(",") {
                            break;
                        }
                    }
                    self.expect_punct(")")?;
                    return Ok(Expr::Call {
                        callee: name,
                        arguments,
                    });
                }
                Ok(Expr::Variable(name))
            }
            Token::Punct(value) if value == "(" => {
                let inner = self.parse_expression()?;
                self.expect_punct(")")?;
                Ok(inner)
            }
            other => Err(JsError::UnexpectedToken {
                found: other.describe(),
                expected: "an expression".to_string(),
            }),
        }
    }

    /// Parses `{ a: 1, "b": 2 }`.
    ///
    /// Keys are identifiers, strings, or numbers, which is what the object
    /// initialiser grammar allows without computed keys. Computed keys,
    /// shorthand, methods, and spread are refused rather than partly handled:
    /// each changes what the initialiser means, not merely how it is written.
    fn parse_object_literal(&mut self) -> Result<Expr, JsError> {
        self.expect_punct("{")?;
        let mut entries = Vec::new();
        while !self.check_punct("}") {
            if self.check_punct("[") {
                return Err(JsError::Unsupported {
                    feature: "computed property keys".to_string(),
                });
            }
            if self.check_punct("...") {
                return Err(JsError::Unsupported {
                    feature: "object spread".to_string(),
                });
            }
            let key = match self.advance() {
                Token::Ident(name) => name,
                Token::Str(text) => text,
                Token::Number(text) => canonical_key(&text),
                other => {
                    return Err(JsError::UnexpectedToken {
                        found: other.describe(),
                        expected: "a property name".to_string(),
                    });
                }
            };
            if !self.eat_punct(":") {
                return Err(JsError::Unsupported {
                    feature: "shorthand and method properties".to_string(),
                });
            }
            entries.push((key, self.parse_assignment()?));
            if !self.eat_punct(",") {
                break;
            }
        }
        self.expect_punct("}")?;
        Ok(Expr::ObjectLiteral { entries })
    }
}

/// Normalises a property key to its string form.
///
/// `o[1]` and `o["1"]` are the same property, so numbers become their canonical
/// string. A number that is not a canonical integer index keeps its ordinary
/// string form, which is what distinguishes `o["01"]` from `o[1]`.
fn canonical_key(text: &str) -> String {
    text.parse::<f64>().map_or_else(
        |_| text.to_string(),
        |number| Value::Number(number).to_string(),
    )
}

/// Whether a key is a canonical array index.
///
/// Enumeration puts these first, in ascending numeric order, ahead of every
/// string key. "01" and "1.0" are not canonical — they are ordinary string keys
/// — which is why this round-trips rather than merely parsing.
///
/// Test-only, because nothing in the language enumerates yet: there is no
/// `for...in` and no `Object.keys`. What ships is the *storage* order that
/// enumeration will read, not enumeration itself, and the distinction is worth
/// keeping visible rather than implying a feature that is not reachable.
#[cfg(test)]
fn array_index(key: &str) -> Option<u32> {
    key.parse::<u32>()
        .ok()
        .filter(|index| index.to_string() == key)
}

/// One object's properties.
///
/// Insertion order is kept because enumeration depends on it, and a map by name
/// is kept because property lookup would otherwise be a linear scan of every
/// property on every access.
#[derive(Clone, Debug, Default, PartialEq)]
struct ObjectData {
    entries: Vec<(String, Value)>,
    index: std::collections::HashMap<String, usize>,
}

impl Trace for ObjectData {
    /// Reports every object this one refers to.
    ///
    /// Exact rather than conservative: the collector learns reachability from
    /// this rather than by guessing which words look like pointers. Missing a
    /// reference here collects a live object, which is the defect this whole
    /// arrangement is built to avoid, so it walks every property value rather
    /// than any subset it believes to be interesting.
    fn trace(&self, out: &mut Vec<GcRef>) {
        for (_, value) in &self.entries {
            if let Value::Object(reference) = value {
                out.push(*reference);
            }
        }
    }
}

impl ObjectData {
    fn get(&self, key: &str) -> Option<&Value> {
        self.index.get(key).map(|&at| &self.entries[at].1)
    }

    /// Sets a property, returning the bytes of key newly stored.
    ///
    /// Assigning to an existing key overwrites in place. Order is a property of
    /// first insertion, so re-assigning must not move the key to the end — the
    /// kind of difference that only shows up when something enumerates.
    fn set(&mut self, key: String, value: Value) -> usize {
        if let Some(&at) = self.index.get(&key) {
            self.entries[at].1 = value;
            return 0;
        }
        let charged = key.len();
        self.index.insert(key.clone(), self.entries.len());
        self.entries.push((key, value));
        charged
    }

    /// Returns keys in the order enumeration will need.
    ///
    /// Integer-like keys ascending first, then the remaining keys in insertion
    /// order. Not the order they were written, and not sorted: a store that
    /// simply kept insertion order, or one that sorted lexicographically, both
    /// look right until a test mixes the two kinds of key.
    ///
    /// Test-only for now, and deliberately so. Nothing in the language reaches
    /// it, so this is the accessor for a property of the representation rather
    /// than an implemented feature. It exists because the ordering constraint
    /// falls on the *store* — a store that lost insertion order could not be
    /// fixed later by the enumerator — and pinning it now costs a test, while
    /// discovering it later costs a rewrite.
    #[cfg(test)]
    fn keys(&self) -> Vec<&str> {
        let mut indexed: Vec<(u32, &str)> = self
            .entries
            .iter()
            .filter_map(|(key, _)| array_index(key).map(|number| (number, key.as_str())))
            .collect();
        indexed.sort_unstable_by_key(|&(number, _)| number);

        let mut keys: Vec<&str> = indexed.into_iter().map(|(_, key)| key).collect();
        keys.extend(
            self.entries
                .iter()
                .filter(|(key, _)| array_index(key).is_none())
                .map(|(key, _)| key.as_str()),
        );
        keys
    }
}

// -- bytecode ------------------------------------------------------------

/// A virtual machine instruction.
#[derive(Clone, Debug, PartialEq)]
pub enum Op {
    /// Push a constant.
    Const(Value),
    /// Push the value of local slot `n`.
    LoadLocal(usize),
    /// Store the top of stack into local slot `n`, leaving it on the stack.
    StoreLocal(usize),
    /// Allocate an empty object and push a handle to it.
    NewObject,
    /// Push a copy of the top of stack.
    Dup,
    /// Call a bound operation by name with `n` arguments from the stack.
    HostCall(String, usize),
    /// Pop key then object; push the property value, or `undefined`.
    GetProperty,
    /// Pop value, key, object; set the property and push the value back.
    SetProperty,
    Add,
    Sub,
    Mul,
    Div,
    Rem,
    Negate,
    Not,
    /// Loose equality, which applies numeric coercion between types.
    Equal,
    /// Strict equality, which requires matching types.
    StrictEqual,
    Less,
    LessEqual,
    Greater,
    GreaterEqual,
    /// Discard the top of stack.
    Pop,
    /// Unconditional jump to an absolute instruction index.
    Jump(usize),
    /// Jump if the top of stack is falsy, consuming it.
    JumpIfFalse(usize),
    /// Jump if falsy, leaving the value for short-circuit operators.
    JumpIfFalsePeek(usize),
    /// Jump if truthy, leaving the value.
    JumpIfTruePeek(usize),
    /// Call function `index` with `argc` arguments from the stack.
    Call {
        index: usize,
        argc: usize,
    },
    /// Return the top of stack from the current function.
    Return,
}

/// A compiled function.
#[derive(Clone, Debug, PartialEq)]
pub struct Function {
    /// Source name, for diagnostics.
    pub name: String,
    /// Parameter count.
    pub arity: usize,
    /// Number of local slots the frame needs.
    pub locals: usize,
    /// Instruction stream.
    pub code: Vec<Op>,
}

/// A compiled program: the top level plus every declared function.
#[derive(Clone, Debug, PartialEq)]
pub struct Program {
    /// Index 0 is the top level.
    pub functions: Vec<Function>,
}

// -- compiler ------------------------------------------------------------

struct Scope {
    names: Vec<(String, bool)>,
    /// Slot index where this scope's names begin.
    base: usize,
}

struct Compiler {
    functions: Vec<Function>,
    /// Function name to table index, resolved for calls.
    signatures: Vec<(String, usize, usize)>,
    scopes: Vec<Scope>,
    code: Vec<Op>,
    next_slot: usize,
    max_slot: usize,
}

impl Compiler {
    fn new() -> Self {
        Self {
            functions: Vec::new(),
            signatures: Vec::new(),
            scopes: Vec::new(),
            code: Vec::new(),
            next_slot: 0,
            max_slot: 0,
        }
    }

    fn compile(mut self, statements: &[Stmt]) -> Result<Program, JsError> {
        // Functions are hoisted so a call can appear before the declaration,
        // and so mutual recursion resolves.
        for statement in statements {
            if let Stmt::Function {
                name, parameters, ..
            } = statement
            {
                let index = self.signatures.len() + 1;
                self.signatures
                    .push((name.clone(), index, parameters.len()));
            }
        }
        // Reserve slot 0 for the top level; function bodies fill 1..n.
        self.functions.push(Function {
            name: "<top>".to_string(),
            arity: 0,
            locals: 0,
            code: Vec::new(),
        });
        for statement in statements {
            if let Stmt::Function {
                name,
                parameters,
                body,
            } = statement
            {
                self.compile_function(name, parameters, body)?;
            }
        }

        self.push_scope();
        for statement in statements {
            if !matches!(statement, Stmt::Function { .. }) {
                self.statement(statement)?;
            }
        }
        self.pop_scope();
        self.code.push(Op::Const(Value::Undefined));
        self.code.push(Op::Return);

        let locals = self.max_slot;
        let code = core::mem::take(&mut self.code);
        self.functions[0] = Function {
            name: "<top>".to_string(),
            arity: 0,
            locals,
            code,
        };
        Ok(Program {
            functions: self.functions,
        })
    }

    fn compile_function(
        &mut self,
        name: &str,
        parameters: &[String],
        body: &[Stmt],
    ) -> Result<(), JsError> {
        let outer_code = core::mem::take(&mut self.code);
        let outer_scopes = core::mem::take(&mut self.scopes);
        let outer_next = self.next_slot;
        let outer_max = self.max_slot;
        self.next_slot = 0;
        self.max_slot = 0;

        self.push_scope();
        for parameter in parameters {
            self.declare(parameter, false);
        }
        for statement in body {
            self.statement(statement)?;
        }
        self.pop_scope();
        // A function without an explicit return yields undefined.
        self.code.push(Op::Const(Value::Undefined));
        self.code.push(Op::Return);

        let function = Function {
            name: name.to_string(),
            arity: parameters.len(),
            locals: self.max_slot,
            code: core::mem::take(&mut self.code),
        };
        self.functions.push(function);

        self.code = outer_code;
        self.scopes = outer_scopes;
        self.next_slot = outer_next;
        self.max_slot = outer_max;
        Ok(())
    }

    fn push_scope(&mut self) {
        self.scopes.push(Scope {
            names: Vec::new(),
            base: self.next_slot,
        });
    }

    fn pop_scope(&mut self) {
        if let Some(scope) = self.scopes.pop() {
            self.next_slot = scope.base;
        }
    }

    fn declare(&mut self, name: &str, constant: bool) -> usize {
        let slot = self.next_slot;
        self.next_slot += 1;
        self.max_slot = self.max_slot.max(self.next_slot);
        if let Some(scope) = self.scopes.last_mut() {
            scope.names.push((name.to_string(), constant));
        }
        slot
    }

    /// Resolves a name to a slot.
    ///
    /// Scopes are walked outermost-first and the last match wins, so an inner
    /// binding shadows an outer one of the same name.
    fn resolve(&self, name: &str) -> Option<(usize, bool)> {
        let mut found = None;
        for scope in &self.scopes {
            for (offset, (candidate, constant)) in scope.names.iter().enumerate() {
                if candidate == name {
                    found = Some((scope.base + offset, *constant));
                }
            }
        }
        found
    }

    fn statement(&mut self, statement: &Stmt) -> Result<(), JsError> {
        match statement {
            Stmt::Declare {
                name,
                value,
                constant,
            } => {
                match value {
                    Some(expression) => self.expression(expression)?,
                    None => self.code.push(Op::Const(Value::Undefined)),
                }
                let slot = self.declare(name, *constant);
                self.code.push(Op::StoreLocal(slot));
                self.code.push(Op::Pop);
            }
            Stmt::Expression(expression) => {
                self.expression(expression)?;
                self.code.push(Op::Pop);
            }
            Stmt::Block(statements) => {
                self.push_scope();
                for inner in statements {
                    self.statement(inner)?;
                }
                self.pop_scope();
            }
            Stmt::If {
                condition,
                then_branch,
                else_branch,
            } => {
                self.expression(condition)?;
                let jump_over_then = self.emit_jump_if_false();
                self.statement(then_branch)?;
                match else_branch {
                    Some(branch) => {
                        let jump_over_else = self.emit_jump();
                        self.patch(jump_over_then);
                        self.statement(branch)?;
                        self.patch(jump_over_else);
                    }
                    None => self.patch(jump_over_then),
                }
            }
            Stmt::While { condition, body } => {
                let loop_start = self.code.len();
                self.expression(condition)?;
                let exit = self.emit_jump_if_false();
                self.statement(body)?;
                self.code.push(Op::Jump(loop_start));
                self.patch(exit);
            }
            Stmt::Return(value) => {
                match value {
                    Some(expression) => self.expression(expression)?,
                    None => self.code.push(Op::Const(Value::Undefined)),
                }
                self.code.push(Op::Return);
            }
            // Nested function declarations would need closures.
            Stmt::Function { .. } => {
                return Err(JsError::Unsupported {
                    feature: "nested function declarations".to_string(),
                });
            }
        }
        Ok(())
    }

    fn expression(&mut self, expression: &Expr) -> Result<(), JsError> {
        match expression {
            Expr::Number(value) => self.code.push(Op::Const(Value::Number(*value))),
            Expr::Str(value) => self.code.push(Op::Const(Value::String(value.clone()))),
            Expr::Boolean(value) => self.code.push(Op::Const(Value::Boolean(*value))),
            Expr::Null => self.code.push(Op::Const(Value::Null)),
            Expr::Undefined => self.code.push(Op::Const(Value::Undefined)),
            Expr::Variable(name) => {
                let (slot, _) = self
                    .resolve(name)
                    .ok_or_else(|| JsError::UndefinedVariable { name: name.clone() })?;
                self.code.push(Op::LoadLocal(slot));
            }
            Expr::Assign { name, value } => {
                let (slot, constant) = self
                    .resolve(name)
                    .ok_or_else(|| JsError::UndefinedVariable { name: name.clone() })?;
                if constant {
                    return Err(JsError::AssignmentToConstant { name: name.clone() });
                }
                self.expression(value)?;
                self.code.push(Op::StoreLocal(slot));
            }
            Expr::Unary { operator, operand } => {
                self.expression(operand)?;
                self.code.push(match operator.as_str() {
                    "-" => Op::Negate,
                    _ => Op::Not,
                });
            }
            Expr::Binary {
                operator,
                left,
                right,
            } => {
                self.expression(left)?;
                self.expression(right)?;
                // `!=` and `!==` compile to the positive comparison followed
                // by a negation, so they need two instructions rather than one.
                let emitted: &[Op] = match operator.as_str() {
                    "+" => &[Op::Add],
                    "-" => &[Op::Sub],
                    "*" => &[Op::Mul],
                    "/" => &[Op::Div],
                    "%" => &[Op::Rem],
                    "==" => &[Op::Equal],
                    "===" => &[Op::StrictEqual],
                    "!=" => &[Op::Equal, Op::Not],
                    "!==" => &[Op::StrictEqual, Op::Not],
                    "<" => &[Op::Less],
                    "<=" => &[Op::LessEqual],
                    ">" => &[Op::Greater],
                    _ => &[Op::GreaterEqual],
                };
                self.code.extend_from_slice(emitted);
            }
            Expr::Logical {
                operator,
                left,
                right,
            } => {
                // Short-circuit: the left value stays on the stack when it
                // decides the result, which is what `a || b` evaluates to.
                self.expression(left)?;
                let jump = if operator == "&&" {
                    self.emit_jump_if_false_peek()
                } else {
                    self.emit_jump_if_true_peek()
                };
                self.code.push(Op::Pop);
                self.expression(right)?;
                self.patch(jump);
            }
            Expr::ObjectLiteral { entries } => {
                self.code.push(Op::NewObject);
                for (key, value) in entries {
                    // SetProperty consumes the object, so each entry works on a
                    // copy and the original stays for the next one. Without the
                    // duplicate the first property empties the stack and every
                    // later access reads a property of `undefined`.
                    self.code.push(Op::Dup);
                    self.code.push(Op::Const(Value::String(key.clone())));
                    self.expression(value)?;
                    self.code.push(Op::SetProperty);
                    // SetProperty leaves the assigned value; drop it so only the
                    // object remains.
                    self.code.push(Op::Pop);
                }
            }
            Expr::Member { object, key } => {
                self.expression(object)?;
                self.expression(key)?;
                self.code.push(Op::GetProperty);
            }
            Expr::SetMember { object, key, value } => {
                self.expression(object)?;
                self.expression(key)?;
                self.expression(value)?;
                self.code.push(Op::SetProperty);
            }
            Expr::Call { callee, arguments } => {
                let Some(&(_, index, arity)) =
                    self.signatures.iter().find(|(name, _, _)| name == callee)
                else {
                    // Not a declared function, so it may be a bound operation.
                    // Script functions are resolved first and therefore win a
                    // name collision: a program's own declaration must not be
                    // shadowed by whatever the embedder happens to expose.
                    //
                    // Whether the name is bound is a property of the host, which
                    // the compiler does not have, so it is checked at the call.
                    for argument in arguments {
                        self.expression(argument)?;
                    }
                    self.code
                        .push(Op::HostCall(callee.clone(), arguments.len()));
                    return Ok(());
                };
                if arguments.len() != arity {
                    return Err(JsError::TypeError {
                        message: format!(
                            "{callee} expects {arity} argument(s), got {}",
                            arguments.len()
                        ),
                    });
                }
                for argument in arguments {
                    self.expression(argument)?;
                }
                self.code.push(Op::Call {
                    index,
                    argc: arguments.len(),
                });
            }
        }
        Ok(())
    }

    fn emit_jump(&mut self) -> usize {
        self.code.push(Op::Jump(usize::MAX));
        self.code.len() - 1
    }

    fn emit_jump_if_false(&mut self) -> usize {
        self.code.push(Op::JumpIfFalse(usize::MAX));
        self.code.len() - 1
    }

    fn emit_jump_if_false_peek(&mut self) -> usize {
        self.code.push(Op::JumpIfFalsePeek(usize::MAX));
        self.code.len() - 1
    }

    fn emit_jump_if_true_peek(&mut self) -> usize {
        self.code.push(Op::JumpIfTruePeek(usize::MAX));
        self.code.len() - 1
    }

    fn patch(&mut self, index: usize) {
        let target = self.code.len();
        match &mut self.code[index] {
            Op::Jump(slot)
            | Op::JumpIfFalse(slot)
            | Op::JumpIfFalsePeek(slot)
            | Op::JumpIfTruePeek(slot) => *slot = target,
            _ => {}
        }
    }
}

/// Compiles `source` into bytecode.
///
/// # Errors
///
/// Returns [`JsError`] for a lexical, syntactic, or unsupported-feature
/// condition. Unsupported features are refused here rather than at run time so
/// that a program which compiles can be trusted to mean what it says.
pub fn compile(source: &str) -> Result<Program, JsError> {
    let tokens = lex(source)?;
    let statements = Parser::new(tokens).parse_program()?;
    Compiler::new().compile(&statements)
}

// -- virtual machine -----------------------------------------------------

/// Executes compiled bytecode.
#[derive(Debug)]
pub struct Vm {
    /// Maximum instructions before execution is abandoned.
    ///
    /// A browser must not let a page wedge the process, so the budget is a
    /// parameter of the machine rather than an afterthought.
    pub step_limit: u64,
    /// Total bytes of string data execution may produce.
    ///
    /// # Why a step limit is not enough
    ///
    /// A step limit bounds how many operations run. It says nothing about how
    /// much any one of them allocates, and `s = s + s` doubles its result every
    /// iteration — so twenty-seven steps of it produced two gigabytes from a
    /// hundred-byte script, using a tiny fraction of the step budget. Bounding
    /// steps and calling memory bounded is the mistake this exists to correct.
    ///
    /// # What it counts
    ///
    /// Bytes produced by concatenation, cumulatively, never credited back when
    /// a value is dropped. Deliberately conservative: tracking live bytes would
    /// need accounting on every drop, and over-counting can only refuse a script
    /// that would otherwise have been allowed, never allow one that should have
    /// been refused. It is a budget for work done, like the step limit beside
    /// it, rather than a measure of resident memory.
    pub byte_limit: u64,
}

impl Default for Vm {
    fn default() -> Self {
        Self {
            step_limit: 1_000_000,
            // Generous for any real script — a megabyte of string building —
            // and far below the point where allocation becomes the attack.
            byte_limit: 1_000_000,
        }
    }
}

impl Vm {
    /// Runs `program` and returns the top-level completion value.
    ///
    /// # Errors
    ///
    /// Returns [`JsError`] on a runtime type error, when the instruction budget
    /// is exhausted, or when the byte budget is exhausted.
    pub fn run(&self, program: &Program) -> Result<Value, JsError> {
        self.run_with_host(program, &mut NoHost::default())
    }

    /// Calls a named function in `program` and returns its value.
    ///
    /// # Why this exists
    ///
    /// The top level's completion value is discarded, so `run` reports nothing
    /// an embedder can use — a script's result was observable only from inside
    /// this crate's own tests. That was a real gap rather than a design: an
    /// embedder that cannot read a result cannot use the interpreter for
    /// anything but side effects it also cannot observe.
    ///
    /// # Errors
    ///
    /// Returns [`JsError::UndefinedVariable`] when no function has that name,
    /// [`JsError::OperationArity`] on an argument-count mismatch, and any error
    /// the call itself produces.
    pub fn call(
        &self,
        program: &Program,
        name: &str,
        arguments: Vec<Value>,
        host: &mut dyn Host,
    ) -> Result<Value, JsError> {
        let Some((index, function)) = program
            .functions
            .iter()
            .enumerate()
            .skip(1)
            .find(|(_, function)| function.name == name)
        else {
            return Err(JsError::UndefinedVariable {
                name: name.to_string(),
            });
        };
        if function.arity != arguments.len() {
            return Err(JsError::OperationArity {
                name: name.to_string(),
                expected: function.arity,
                got: arguments.len(),
            });
        }
        let mut runtime = Runtime::default();
        self.run_function(program, index, arguments, &mut runtime, host)
    }

    /// Runs `program` with `host` supplying the bound operations.
    ///
    /// # Errors
    ///
    /// Returns [`JsError`] on a runtime type error, an exhausted budget, or a
    /// call to an operation the host does not expose.
    pub fn run_with_host(&self, program: &Program, host: &mut dyn Host) -> Result<Value, JsError> {
        // One heap for the whole run, so a reference stays meaningful across
        // calls.
        let mut runtime = Runtime::default();
        self.run_function(program, 0, Vec::new(), &mut runtime, host)
    }

    fn run_function(
        &self,
        program: &Program,
        index: usize,
        arguments: Vec<Value>,
        runtime: &mut Runtime,
        host: &mut dyn Host,
    ) -> Result<Value, JsError> {
        let function = &program.functions[index];
        let mut locals = vec![Value::Undefined; function.locals.max(arguments.len())];
        for (slot, argument) in arguments.into_iter().enumerate() {
            locals[slot] = argument;
        }
        let mut stack: Vec<Value> = Vec::new();
        let mut pointer = 0_usize;

        while pointer < function.code.len() {
            runtime.steps += 1;
            if runtime.steps > self.step_limit {
                return Err(JsError::StepLimitExceeded {
                    limit: self.step_limit,
                });
            }
            match &function.code[pointer] {
                Op::Const(value) => stack.push(value.clone()),
                Op::LoadLocal(slot) => {
                    stack.push(locals.get(*slot).cloned().unwrap_or(Value::Undefined));
                }
                Op::StoreLocal(slot) => {
                    let value = stack.last().cloned().unwrap_or(Value::Undefined);
                    if *slot >= locals.len() {
                        locals.resize(slot + 1, Value::Undefined);
                    }
                    locals[*slot] = value;
                }
                Op::Pop => {
                    stack.pop();
                }
                Op::Add => {
                    let right = pop(&mut stack);
                    let left = pop(&mut stack);
                    // `+` concatenates when either side is a string, which is
                    // the one arithmetic operator that is not purely numeric.
                    let result = match (&left, &right) {
                        (Value::String(_), _) | (_, Value::String(_)) => {
                            let joined = format!("{left}{right}");
                            // Charged after building, because the operands are
                            // already resident and the result is at most their
                            // sum — there is no oversized intermediate to avoid,
                            // and the budget is what stops the next doubling.
                            runtime.bytes = runtime.bytes.saturating_add(joined.len() as u64);
                            if runtime.bytes > self.byte_limit {
                                return Err(JsError::ByteLimitExceeded {
                                    limit: self.byte_limit,
                                });
                            }
                            Value::String(joined)
                        }
                        _ => Value::Number(to_number(&left) + to_number(&right)),
                    };
                    stack.push(result);
                }
                Op::HostCall(name, count) => {
                    let mut arguments = Vec::with_capacity(*count);
                    for _ in 0..*count {
                        arguments.push(pop(&mut stack));
                    }
                    arguments.reverse();

                    // Resolution goes through the registry the host publishes,
                    // so the callable set and the auditable set are one table
                    // and cannot drift apart.
                    let operation = host
                        .bindings()
                        .resolve_global(name)
                        .map_err(|_| JsError::UnboundOperation { name: name.clone() })?;
                    if operation.arity != arguments.len() {
                        return Err(JsError::OperationArity {
                            name: name.clone(),
                            expected: operation.arity,
                            got: arguments.len(),
                        });
                    }
                    let interface = operation.interface.clone();
                    let value = host
                        .invoke(&interface, name, &arguments)
                        .map_err(|message| JsError::HostOperationFailed {
                            name: name.clone(),
                            message,
                        })?;
                    stack.push(value);
                }
                Op::Dup => {
                    let top = stack.last().cloned().unwrap_or(Value::Undefined);
                    stack.push(top);
                }
                Op::NewObject => {
                    // Charged like any other produced data. Objects were named
                    // as a future amplification path when the byte budget was
                    // added; this is that path, so it is charged from the start
                    // rather than after someone finds the loop that exploits it.
                    runtime.bytes = runtime.bytes.saturating_add(OBJECT_OVERHEAD_BYTES);
                    if runtime.bytes > self.byte_limit {
                        return Err(JsError::ByteLimitExceeded {
                            limit: self.byte_limit,
                        });
                    }
                    // A safepoint. Collecting here is safe because every live
                    // value is reachable: the frames above published theirs
                    // into `runtime.outer`, and this frame's are right here.
                    if runtime.heap.occupied_slots() >= COLLECT_AFTER_ALLOCATIONS {
                        collect_now(runtime, &stack, &locals);
                    }
                    let reference =
                        runtime
                            .heap
                            .allocate(ObjectData::default())
                            .map_err(|error| JsError::TypeError {
                                message: error.to_string(),
                            })?;
                    stack.push(Value::Object(reference));
                }
                Op::GetProperty => {
                    let key = pop(&mut stack);
                    let object = pop(&mut stack);
                    let Value::Object(handle) = object else {
                        return Err(JsError::TypeError {
                            message: format!("cannot access a property of {object}"),
                        });
                    };
                    // A missing property reads `undefined`. This is the one
                    // lookup in this workspace that is not a typed refusal, and
                    // it is specified: absence is an ordinary result here, not
                    // a gap in the implementation.
                    let object = runtime
                        .heap
                        .get(handle)
                        .map_err(|error| JsError::TypeError {
                            message: error.to_string(),
                        })?;
                    let value = object
                        .get(&property_key(&key))
                        .cloned()
                        .unwrap_or(Value::Undefined);
                    stack.push(value);
                }
                Op::SetProperty => {
                    let value = pop(&mut stack);
                    let key = pop(&mut stack);
                    let object = pop(&mut stack);
                    let Value::Object(handle) = object else {
                        return Err(JsError::TypeError {
                            message: format!("cannot access a property of {object}"),
                        });
                    };
                    let object =
                        runtime
                            .heap
                            .get_mut(handle)
                            .map_err(|error| JsError::TypeError {
                                message: error.to_string(),
                            })?;
                    let charged = object.set(property_key(&key), value.clone());
                    runtime.bytes = runtime.bytes.saturating_add(charged as u64);
                    if runtime.bytes > self.byte_limit {
                        return Err(JsError::ByteLimitExceeded {
                            limit: self.byte_limit,
                        });
                    }
                    stack.push(value);
                }
                Op::Sub => binary_number(&mut stack, |a, b| a - b),
                Op::Mul => binary_number(&mut stack, |a, b| a * b),
                Op::Div => binary_number(&mut stack, |a, b| a / b),
                Op::Rem => binary_number(&mut stack, |a, b| a % b),
                Op::Negate => {
                    let value = pop(&mut stack);
                    stack.push(Value::Number(-to_number(&value)));
                }
                Op::Not => {
                    let value = pop(&mut stack);
                    stack.push(Value::Boolean(!value.truthy()));
                }
                Op::Equal => {
                    let right = pop(&mut stack);
                    let left = pop(&mut stack);
                    stack.push(Value::Boolean(loose_equal(&left, &right)));
                }
                Op::StrictEqual => {
                    let right = pop(&mut stack);
                    let left = pop(&mut stack);
                    stack.push(Value::Boolean(strict_equal(&left, &right)));
                }
                Op::Less => compare(&mut stack, |ordering| ordering < 0),
                Op::LessEqual => compare(&mut stack, |ordering| ordering <= 0),
                Op::Greater => compare(&mut stack, |ordering| ordering > 0),
                Op::GreaterEqual => compare(&mut stack, |ordering| ordering >= 0),
                Op::Jump(target) => {
                    pointer = *target;
                    continue;
                }
                Op::JumpIfFalse(target) => {
                    let value = pop(&mut stack);
                    if !value.truthy() {
                        pointer = *target;
                        continue;
                    }
                }
                Op::JumpIfFalsePeek(target) => {
                    if !stack.last().is_some_and(Value::truthy) {
                        pointer = *target;
                        continue;
                    }
                }
                Op::JumpIfTruePeek(target) => {
                    if stack.last().is_some_and(Value::truthy) {
                        pointer = *target;
                        continue;
                    }
                }
                Op::Call { index, argc } => {
                    let split = stack.len().saturating_sub(*argc);
                    let arguments = stack.split_off(split);
                    let result = {
                        // Publish this frame's live values before recursing, so
                        // a collection inside the call can see them, and drop
                        // them again afterwards.
                        let restore = runtime.outer.len();
                        runtime.outer.extend(stack.iter().cloned());
                        runtime.outer.extend(locals.iter().cloned());
                        let outcome = self.run_function(program, *index, arguments, runtime, host);
                        runtime.outer.truncate(restore);
                        outcome
                    }?;
                    stack.push(result);
                }
                Op::Return => return Ok(pop(&mut stack)),
            }
            pointer += 1;
        }
        Ok(Value::Undefined)
    }
}

fn pop(stack: &mut Vec<Value>) -> Value {
    stack.pop().unwrap_or(Value::Undefined)
}

fn binary_number(stack: &mut Vec<Value>, operation: fn(f64, f64) -> f64) {
    let right = pop(stack);
    let left = pop(stack);
    stack.push(Value::Number(operation(
        to_number(&left),
        to_number(&right),
    )));
}

fn compare(stack: &mut Vec<Value>, decide: fn(i32) -> bool) {
    let right = pop(stack);
    let left = pop(stack);
    let (a, b) = (to_number(&left), to_number(&right));
    // Any comparison with NaN is false, including NaN <= NaN.
    if a.is_nan() || b.is_nan() {
        stack.push(Value::Boolean(false));
        return;
    }
    let ordering = if a < b {
        -1
    } else if a > b {
        1
    } else {
        0
    };
    stack.push(Value::Boolean(decide(ordering)));
}

/// Roots the live value set and collects.
///
/// The root set is assembled fresh each time rather than maintained: a root
/// registered once and forgotten keeps its object alive forever, and this
/// interpreter's values move between stack slots constantly. Registering,
/// collecting, and clearing is more work per collection and cannot leak a root.
fn collect_now(runtime: &mut Runtime, stack: &[Value], locals: &[Value]) {
    let live = runtime
        .outer
        .iter()
        .chain(stack)
        .chain(locals)
        .filter_map(|value| match value {
            Value::Object(reference) => Some(*reference),
            _ => None,
        })
        .collect::<Vec<_>>();

    for reference in &live {
        runtime.heap.add_root(*reference);
    }
    runtime.heap.collect();
    for reference in &live {
        runtime.heap.remove_root(*reference);
    }
}

/// What the interpreter needs from its embedder to call out of the script.
///
/// # Why a trait rather than a dependency
///
/// The interpreter must not know what a DOM is, the same way selector matching
/// must not know what `turing-html` is. An embedder exposing something else
/// entirely — a test double, a different document model, a restricted subset
/// for an untrusted principal — implements this and nothing changes here.
///
/// # Why the registry is part of the contract
///
/// `REQ-AI-001` treats agents as separately identified principals, and the
/// blueprint's justification for a registry rather than direct calls is that a
/// capability which cannot be listed cannot be granted or revoked. That only
/// holds if the callable set and the listed set are the *same* set, so
/// invocation here resolves through [`Host::bindings`] rather than through any
/// separate dispatch table. There is no path by which a host can expose an
/// operation that auditing would not show.
pub trait Host {
    /// Returns the operations this host exposes.
    fn bindings(&self) -> &Bindings;

    /// Performs a bound operation.
    ///
    /// Only ever called after the operation resolved in [`Host::bindings`] and
    /// its arity matched, so an implementation does not repeat those checks.
    ///
    /// # Errors
    ///
    /// Returns a message describing why the operation could not be performed.
    fn invoke(&mut self, interface: &str, name: &str, arguments: &[Value])
    -> Result<Value, String>;
}

/// A host exposing nothing.
///
/// The default, so a script that calls out fails with an unbound operation
/// rather than the interpreter having to treat "no host" as a special case.
#[derive(Debug, Default)]
pub struct NoHost {
    bindings: Bindings,
}

impl Host for NoHost {
    fn bindings(&self) -> &Bindings {
        &self.bindings
    }

    fn invoke(
        &mut self,
        _interface: &str,
        name: &str,
        _arguments: &[Value],
    ) -> Result<Value, String> {
        // Unreachable through the interpreter, which resolves first against an
        // empty registry. Stated rather than left to `unreachable!`, which would
        // turn a future dispatch mistake into a panic.
        Err(format!("{name} is not bound: this host exposes nothing"))
    }
}

/// Everything a running program owns that outlives a single instruction.
///
/// # Why the outer frames are here
///
/// Collection has to see every live value, and each call frame owns its own
/// operand stack and locals. A collection triggered inside a nested call cannot
/// reach the frames above it, so those frames publish their values here before
/// recursing and truncate afterwards. Without that, an object held only by a
/// caller is unreachable at the moment the callee allocates, and the collector
/// is correct to free it — which is exactly how a rooting bug frees live data
/// while every shallow test passes.
#[derive(Debug, Default)]
struct Runtime {
    heap: Heap<ObjectData>,
    /// Values held by call frames above the one currently executing.
    outer: Vec<Value>,
    steps: u64,
    bytes: u64,
}

/// How many objects may be allocated before a collection is attempted.
///
/// A trigger, not a limit. Small enough that ordinary programs collect during a
/// run rather than only at the end, because a collector that never runs in
/// tests is a collector nobody has tested.
const COLLECT_AFTER_ALLOCATIONS: usize = 64;

/// Bytes charged for creating an object, before any property is added.
///
/// A stand-in for the real cost of a map and a vector rather than a measured
/// figure. Its purpose is that allocating objects in a loop is charged at all,
/// not that the number is accurate.
const OBJECT_OVERHEAD_BYTES: u64 = 64;

/// Converts a value used as a property key into its string form.
///
/// `o[1]` and `o["1"]` name the same property, so a numeric key becomes its
/// canonical string. Everything else uses its ordinary string form.
fn property_key(value: &Value) -> String {
    value.to_string()
}

fn to_number(value: &Value) -> f64 {
    match value {
        Value::Number(number) => *number,
        Value::Boolean(true) => 1.0,
        Value::Boolean(false) | Value::Null => 0.0,
        Value::String(text) => text.trim().parse::<f64>().unwrap_or(f64::NAN),
        // An object would coerce through `valueOf`/`toString`, which needs a
        // prototype chain this implementation does not model, so it is NaN
        // rather than a guessed conversion.
        Value::Undefined | Value::Function(_) | Value::Object(_) => f64::NAN,
    }
}

fn strict_equal(left: &Value, right: &Value) -> bool {
    match (left, right) {
        // NaN is not equal to itself under either equality operator.
        (Value::Number(a), Value::Number(b)) => a == b,
        (Value::String(a), Value::String(b)) => a == b,
        (Value::Boolean(a), Value::Boolean(b)) => a == b,
        (Value::Null, Value::Null) | (Value::Undefined, Value::Undefined) => true,
        (Value::Function(a), Value::Function(b)) => a == b,
        // Objects compare by identity, not contents: two objects with the same
        // properties are different objects. Comparing contents would also not
        // terminate on a self-referential one.
        (Value::Object(a), Value::Object(b)) => a == b,
        _ => false,
    }
}

fn loose_equal(left: &Value, right: &Value) -> bool {
    match (left, right) {
        // null and undefined are loosely equal to each other and nothing else.
        (Value::Null | Value::Undefined, Value::Null | Value::Undefined) => true,
        (Value::Null | Value::Undefined, _) | (_, Value::Null | Value::Undefined) => false,
        (Value::String(a), Value::String(b)) => a == b,
        _ => {
            let (a, b) = (to_number(left), to_number(right));
            !a.is_nan() && !b.is_nan() && a == b
        }
    }
}

/// Compiles and runs `source`, returning the completion value.
///
/// # Errors
///
/// Returns [`JsError`] from compilation or execution.
pub fn evaluate(source: &str) -> Result<Value, JsError> {
    let program = compile(source)?;
    Vm::default().run(&program)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn run(source: &str) -> Value {
        evaluate(source).expect("evaluates")
    }

    /// Compiles and runs `source`, calling `main` directly.
    fn run_main_source(source: &str) -> Value {
        let program = compile(source).expect("compiles");
        Vm::default()
            .run_function(
                &program,
                1,
                Vec::new(),
                &mut Runtime::default(),
                &mut NoHost::default(),
            )
            .expect("runs")
    }

    /// Runs `body` as the whole of `main` and returns what it returns.
    ///
    /// Separate from `expr` because a nested `function` declaration is refused,
    /// so a test needing statements cannot wrap them in another function.
    fn run_main(body: &str) -> Value {
        let program = compile(&format!("function main() {{ {body} }} main();")).expect("compiles");
        Vm::default()
            .run_function(
                &program,
                1,
                Vec::new(),
                &mut Runtime::default(),
                &mut NoHost::default(),
            )
            .expect("runs")
    }

    /// Evaluates an expression by binding it and returning the binding.
    fn expr(source: &str) -> Value {
        let wrapped = format!("function main() {{ return {source}; }}");
        let program = compile(&format!("{wrapped} main();")).expect("compiles");
        // The top level's last value is discarded, so call directly.
        Vm::default()
            .run_function(
                &program,
                1,
                Vec::new(),
                &mut Runtime::default(),
                &mut NoHost::default(),
            )
            .expect("runs")
    }

    #[test]
    fn evaluates_arithmetic_with_precedence() {
        assert_eq!(expr("1 + 2 * 3"), Value::Number(7.0));
        assert_eq!(expr("(1 + 2) * 3"), Value::Number(9.0));
        assert_eq!(expr("7 % 4"), Value::Number(3.0));
        assert_eq!(expr("-3 + 1"), Value::Number(-2.0));
    }

    #[test]
    fn string_concatenation_uses_plus() {
        assert_eq!(expr("\"a\" + \"b\""), Value::String("ab".to_string()));
        // A string on either side makes `+` concatenate rather than add.
        assert_eq!(expr("1 + \"a\""), Value::String("1a".to_string()));
    }

    #[test]
    fn strict_and_loose_equality_differ() {
        assert_eq!(expr("1 == \"1\""), Value::Boolean(true));
        assert_eq!(expr("1 === \"1\""), Value::Boolean(false));
        assert_eq!(expr("1 != \"1\""), Value::Boolean(false));
        assert_eq!(expr("1 !== \"1\""), Value::Boolean(true));
    }

    #[test]
    fn null_and_undefined_are_loosely_equal_only_to_each_other() {
        assert_eq!(expr("null == undefined"), Value::Boolean(true));
        assert_eq!(expr("null === undefined"), Value::Boolean(false));
        assert_eq!(expr("null == 0"), Value::Boolean(false));
    }

    #[test]
    fn comparisons_with_nan_are_always_false() {
        // Including NaN <= NaN, which a naive ordering implementation gets
        // wrong by returning true.
        assert_eq!(expr("0 / 0 < 1"), Value::Boolean(false));
        assert_eq!(expr("0 / 0 <= 0 / 0"), Value::Boolean(false));
        assert_eq!(expr("0 / 0 === 0 / 0"), Value::Boolean(false));
    }

    #[test]
    fn truthiness_follows_the_specification() {
        assert_eq!(expr("!0"), Value::Boolean(true));
        assert_eq!(expr("!\"\""), Value::Boolean(true));
        assert_eq!(expr("!\"a\""), Value::Boolean(false));
        assert_eq!(expr("!null"), Value::Boolean(true));
        assert_eq!(expr("!(0 / 0)"), Value::Boolean(true));
    }

    #[test]
    fn logical_operators_short_circuit_and_yield_operands() {
        // `a || b` evaluates to an operand, not to a boolean.
        assert_eq!(expr("0 || 5"), Value::Number(5.0));
        assert_eq!(expr("3 || 5"), Value::Number(3.0));
        assert_eq!(expr("0 && 5"), Value::Number(0.0));
        assert_eq!(expr("3 && 5"), Value::Number(5.0));
    }

    #[test]
    fn bindings_and_assignment_work() {
        assert_eq!(
            run("let a = 1; let b = 2; function f() { return 0; } a = a + b;"),
            Value::Undefined
        );
        let program =
            compile("function f() { let a = 1; a = a + 4; return a; } f();").expect("compiles");
        assert_eq!(
            Vm::default()
                .run_function(
                    &program,
                    1,
                    Vec::new(),
                    &mut Runtime::default(),
                    &mut NoHost::default()
                )
                .expect("runs"),
            Value::Number(5.0)
        );
    }

    #[test]
    fn if_else_selects_the_right_branch() {
        let program =
            compile("function f() { if (1 > 2) { return 10; } else { return 20; } } f();")
                .expect("compiles");
        assert_eq!(
            Vm::default()
                .run_function(
                    &program,
                    1,
                    Vec::new(),
                    &mut Runtime::default(),
                    &mut NoHost::default()
                )
                .expect("runs"),
            Value::Number(20.0)
        );
    }

    #[test]
    fn while_loops_iterate() {
        let program = compile(
            "function sum() { let i = 0; let total = 0; \
             while (i < 5) { total = total + i; i = i + 1; } return total; } sum();",
        )
        .expect("compiles");
        assert_eq!(
            Vm::default()
                .run_function(
                    &program,
                    1,
                    Vec::new(),
                    &mut Runtime::default(),
                    &mut NoHost::default()
                )
                .expect("runs"),
            Value::Number(10.0)
        );
    }

    #[test]
    fn functions_take_arguments_and_return() {
        let program =
            compile("function add(a, b) { return a + b; } function main() { return add(2, 3); }")
                .expect("compiles");
        assert_eq!(
            Vm::default()
                .run_function(
                    &program,
                    2,
                    Vec::new(),
                    &mut Runtime::default(),
                    &mut NoHost::default()
                )
                .expect("runs"),
            Value::Number(5.0)
        );
    }

    #[test]
    fn recursion_works() {
        let program = compile(
            "function fact(n) { if (n <= 1) { return 1; } return n * fact(n - 1); } \
             function main() { return fact(5); }",
        )
        .expect("compiles");
        assert_eq!(
            Vm::default()
                .run_function(
                    &program,
                    2,
                    Vec::new(),
                    &mut Runtime::default(),
                    &mut NoHost::default()
                )
                .expect("runs"),
            Value::Number(120.0)
        );
    }

    #[test]
    fn functions_are_hoisted_so_calls_may_precede_declarations() {
        let program = compile("function main() { return later(); } function later() { return 7; }")
            .expect("compiles");
        assert_eq!(
            Vm::default()
                .run_function(
                    &program,
                    1,
                    Vec::new(),
                    &mut Runtime::default(),
                    &mut NoHost::default()
                )
                .expect("runs"),
            Value::Number(7.0)
        );
    }

    #[test]
    fn a_function_without_return_yields_undefined() {
        let program = compile("function f() { let a = 1; } f();").expect("compiles");
        assert_eq!(
            Vm::default()
                .run_function(
                    &program,
                    1,
                    Vec::new(),
                    &mut Runtime::default(),
                    &mut NoHost::default()
                )
                .expect("runs"),
            Value::Undefined
        );
    }

    #[test]
    fn block_scope_is_respected() {
        // The inner `a` must not leak out of its block.
        let program =
            compile("function f() { let a = 1; { let a = 2; } return a; } f();").expect("compiles");
        assert_eq!(
            Vm::default()
                .run_function(
                    &program,
                    1,
                    Vec::new(),
                    &mut Runtime::default(),
                    &mut NoHost::default()
                )
                .expect("runs"),
            Value::Number(1.0)
        );
    }

    #[test]
    fn undefined_variables_are_refused_at_compile_time() {
        let error = compile("let a = b + 1;").expect_err("refused");
        assert!(matches!(error, JsError::UndefinedVariable { .. }));
    }

    #[test]
    fn assignment_to_const_is_refused() {
        let error = compile("const a = 1; a = 2;").expect_err("refused");
        assert!(matches!(error, JsError::AssignmentToConstant { .. }));
    }

    #[test]
    fn wrong_argument_count_is_refused() {
        let error = compile("function f(a, b) { return a; } function main() { return f(1); }")
            .expect_err("refused");
        assert!(matches!(error, JsError::TypeError { .. }));
    }

    #[test]
    fn an_infinite_loop_hits_the_step_limit() {
        // A browser must not let a page wedge the process.
        let program = compile("function f() { while (true) { } } f();").expect("compiles");
        let vm = Vm {
            step_limit: 10_000,
            ..Vm::default()
        };
        let error = vm
            .run_function(
                &program,
                1,
                Vec::new(),
                &mut Runtime::default(),
                &mut NoHost::default(),
            )
            .expect_err("aborted");
        assert!(matches!(error, JsError::StepLimitExceeded { .. }));
    }

    #[test]
    fn unsupported_features_are_refused_not_partially_evaluated() {
        for (source, label) in [
            ("class A {}", "class"),
            ("try { } catch (e) { }", "try"),
            ("async function f() {}", "async"),
            ("for (;;) {}", "for"),
            ("new Thing();", "new"),
            ("import x from \"y\";", "import"),
            ("switch (a) {}", "switch"),
        ] {
            let error = compile(source).expect_err(label);
            assert!(
                matches!(error, JsError::Unsupported { .. }),
                "{label} was not refused: {error:?}"
            );
        }
    }

    #[test]
    fn property_access_and_arrays_are_refused() {
        // `.` and `[` are not lexed, so these fail rather than misparsing.
        assert!(compile("let a = b.c;").is_err());
        assert!(compile("let a = [1, 2];").is_err());
    }

    #[test]
    fn comments_are_ignored() {
        let program =
            compile("// leading\nfunction f() { /* inner */ return 1; } f();").expect("compiles");
        assert_eq!(
            Vm::default()
                .run_function(
                    &program,
                    1,
                    Vec::new(),
                    &mut Runtime::default(),
                    &mut NoHost::default()
                )
                .expect("runs"),
            Value::Number(1.0)
        );
    }

    #[test]
    fn compiles_to_a_flat_instruction_stream() {
        // The bytecode shape is the point of WP-010; assert it exists.
        let program = compile("function f() { return 1 + 2; }").expect("compiles");
        let code = &program.functions[1].code;
        assert!(code.contains(&Op::Add), "{code:?}");
        assert!(code.contains(&Op::Return), "{code:?}");
    }
    // -- objects ---------------------------------------------------------

    #[test]
    fn reads_and_writes_properties() {
        assert_eq!(expr("({ a: 1 }).a"), Value::Number(1.0));
        assert_eq!(expr("({ a: 1, b: 2 }).b"), Value::Number(2.0));
    }

    #[test]
    fn a_missing_property_reads_undefined() {
        // The one lookup here that is not a typed refusal. Absence is an
        // ordinary specified result rather than a gap in the implementation, so
        // erring would be wrong even though it matches this workspace's habit.
        assert_eq!(expr("({ a: 1 }).missing"), Value::Undefined);
        assert_eq!(expr("({}).anything"), Value::Undefined);
    }

    #[test]
    fn bracket_and_dot_access_name_the_same_property() {
        assert_eq!(expr("({ a: 1 })['a']"), Value::Number(1.0));
    }

    #[test]
    fn a_numeric_key_and_its_string_form_are_one_property() {
        // `o[1]` and `o["1"]` are the same property. Treating the number as a
        // distinct key gives every integer-keyed object two of everything, and
        // reads still succeed, so nothing looks wrong.
        assert_eq!(
            expr("({ 1: 'first' })['1']"),
            Value::String("first".to_string())
        );
        assert_eq!(
            expr("({ 1: 'first' })[1]"),
            Value::String("first".to_string())
        );
    }

    #[test]
    fn assignment_creates_and_updates_properties() {
        assert_eq!(
            run_main("let o = {}; o.a = 5; return o.a;"),
            Value::Number(5.0)
        );
        assert_eq!(
            run_main("let o = { a: 1 }; o.a = 9; return o.a;"),
            Value::Number(9.0)
        );
    }

    #[test]
    fn an_object_is_a_handle_not_a_copy() {
        // Two names for one object must see each other's writes. A store that
        // cloned on assignment would pass every single-name test.
        assert_eq!(
            run_main("let a = {}; let b = a; b.x = 3; return a.x;"),
            Value::Number(3.0)
        );
    }

    #[test]
    fn an_object_can_refer_to_itself() {
        // The reason objects are handles rather than owned values: an owned
        // representation would not terminate here.
        assert_eq!(
            run_main("let o = {}; o.self = o; return o.self.self.self === o;"),
            Value::Boolean(true)
        );
    }

    #[test]
    fn enumeration_puts_integer_keys_first_in_numeric_order() {
        // The order is integer-like keys ascending, then the rest in insertion
        // order. A store keeping only insertion order, and one sorting keys
        // lexicographically, both look correct until a test mixes the two kinds
        // — and lexicographic order would also put "10" before "2".
        let mut object = ObjectData::default();
        for key in ["2", "b", "10", "a", "1"] {
            object.set(key.to_string(), Value::Number(0.0));
        }
        assert_eq!(object.keys(), vec!["1", "2", "10", "b", "a"]);
    }

    #[test]
    fn a_non_canonical_numeric_key_is_an_ordinary_string_key() {
        // "01" and "1.0" parse as numbers but are not canonical array indices,
        // so they enumerate with the string keys rather than being reordered.
        let mut object = ObjectData::default();
        for key in ["01", "1", "1.0"] {
            object.set(key.to_string(), Value::Number(0.0));
        }
        assert_eq!(object.keys(), vec!["1", "01", "1.0"]);
    }

    #[test]
    fn reassignment_keeps_a_key_in_its_original_position() {
        // Order belongs to first insertion. Re-assigning through a path that
        // removes and re-appends would move the key to the end, which only
        // shows up when something enumerates.
        let mut object = ObjectData::default();
        object.set("a".to_string(), Value::Number(1.0));
        object.set("b".to_string(), Value::Number(2.0));
        object.set("a".to_string(), Value::Number(3.0));

        assert_eq!(object.keys(), vec!["a", "b"]);
        assert_eq!(object.get("a"), Some(&Value::Number(3.0)));
    }

    #[test]
    fn reassignment_is_not_charged_again() {
        // Only a new key stores anything. Charging every assignment would let
        // an ordinary loop exhaust the budget.
        let mut object = ObjectData::default();
        assert_eq!(object.set("key".to_string(), Value::Number(1.0)), 3);
        assert_eq!(object.set("key".to_string(), Value::Number(2.0)), 0);
    }

    #[test]
    fn allocating_objects_in_a_loop_is_charged() {
        // Objects were named as a future amplification path when the byte
        // budget was added. This is that path, charged from the start rather
        // than after someone finds the loop that exploits it.
        let source = "function main() { let i = 0; let o = {}; \
                      while (i < 100000) { o = {}; i = i + 1; } return o; } main();";
        assert!(matches!(
            evaluate(source),
            Err(JsError::ByteLimitExceeded { .. })
        ));
    }

    #[test]
    fn a_modest_number_of_objects_is_allowed() {
        // The other side of the bracket: a budget that refused ordinary object
        // use would pass the test above and be useless.
        let source = "function main() { let i = 0; let o = {}; \
                      while (i < 100) { o = {}; i = i + 1; } return o; } main();";
        assert!(evaluate(source).is_ok());
    }

    #[test]
    fn a_property_access_on_a_non_object_is_a_type_error() {
        assert!(matches!(
            evaluate("function main() { let n = 1; return n.a; } main();"),
            Err(JsError::TypeError { .. })
        ));
    }

    #[test]
    fn an_object_is_truthy_even_when_empty() {
        // The case people expect to behave like an empty string, and it does
        // not.
        // `&&` yields its right operand when the left is truthy.
        assert_eq!(expr("({}) && 1"), Value::Number(1.0));
    }

    #[test]
    fn unmodelled_object_syntax_is_refused() {
        // Each of these changes what an initialiser means rather than only how
        // it is written, so a partial implementation would silently drop
        // properties the author wrote.
        for source in [
            "let o = { ['computed']: 1 };",
            "let a = 1; let o = { a };",
            "let o = { m() { return 1; } };",
        ] {
            assert!(
                matches!(compile(source), Err(JsError::Unsupported { .. })),
                "expected a refusal for {source}"
            );
        }
    }
    // -- collection ------------------------------------------------------

    /// Allocates well past the collection trigger, so any test using it is
    /// guaranteed to have collected at least once.
    ///
    /// Without this every test below would pass on an interpreter that never
    /// collects, which is the state the previous iteration shipped.
    fn allocations_beyond_trigger() -> usize {
        COLLECT_AFTER_ALLOCATIONS * 4
    }

    #[test]
    fn a_live_object_in_a_local_survives_collection() {
        // The acceptance test for the wiring. A rooting protocol that missed
        // locals would free `kept` here and the generation check would turn the
        // later read into a dangling-reference error rather than the value.
        let source = format!(
            "function main() {{ let kept = {{}}; kept.mark = 7; let i = 0; \
             while (i < {}) {{ let junk = {{}}; i = i + 1; }} return kept.mark; }} main();",
            allocations_beyond_trigger()
        );
        assert_eq!(run_main_source(&source), Value::Number(7.0));
    }

    #[test]
    fn a_live_object_on_the_operand_stack_survives_collection() {
        // Locals are the obvious root; the operand stack is the one an
        // implementation forgets. Here the outer object is mid-expression —
        // held only on the stack — while the inner initialiser allocates past
        // the trigger.
        let source = format!(
            "function main() {{ let n = 0; let o = {{ a: helper(), b: 2 }}; \
             return o.b; }} \
             function helper() {{ let i = 0; \
             while (i < {}) {{ let junk = {{}}; i = i + 1; }} return 1; }} main();",
            allocations_beyond_trigger()
        );
        assert_eq!(run_main_source(&source), Value::Number(2.0));
    }

    #[test]
    fn an_object_held_only_by_a_caller_survives_a_collection_in_the_callee() {
        // The frames above the one executing publish their values before
        // recursing. Without that this object is unreachable at the moment the
        // callee allocates, and the collector is *correct* to free it — the
        // failure looks like a collector bug and is a rooting bug.
        let source = format!(
            "function main() {{ let held = {{}}; held.mark = 5; \
             let ignored = churn(); return held.mark; }} \
             function churn() {{ let i = 0; \
             while (i < {}) {{ let junk = {{}}; i = i + 1; }} return 0; }} main();",
            allocations_beyond_trigger()
        );
        assert_eq!(run_main_source(&source), Value::Number(5.0));
    }

    #[test]
    fn a_reachable_chain_survives_collection() {
        // Reachability is transitive, which is what `Trace` on the object is
        // for. A collector that rooted only the values it could see directly
        // would free the far end of this chain.
        let source = format!(
            "function main() {{ let root = {{}}; let mid = {{}}; let leaf = {{}}; \
             leaf.mark = 11; mid.next = leaf; root.next = mid; \
             mid = 0; leaf = 0; \
             let i = 0; while (i < {}) {{ let junk = {{}}; i = i + 1; }} \
             return root.next.next.mark; }} main();",
            allocations_beyond_trigger()
        );
        assert_eq!(run_main_source(&source), Value::Number(11.0));
    }

    #[test]
    fn unreachable_objects_are_actually_reclaimed() {
        // The other half. Every test above would also pass on a collector that
        // never frees anything, so this asserts that slots are reused: without
        // reclamation the heap would hold every object ever allocated.
        let allocations = allocations_beyond_trigger();
        let source = format!(
            "function main() {{ let i = 0; \
             while (i < {allocations}) {{ let junk = {{}}; i = i + 1; }} return 0; }} main();"
        );
        let program = compile(&source).expect("compiles");
        let mut runtime = Runtime::default();
        Vm::default()
            .run_function(
                &program,
                1,
                Vec::new(),
                &mut runtime,
                &mut NoHost::default(),
            )
            .expect("runs");

        assert!(
            runtime.heap.occupied_slots() < allocations,
            "{} slots occupied after {allocations} allocations; nothing was reclaimed",
            runtime.heap.occupied_slots()
        );
    }

    #[test]
    fn an_unreachable_cycle_is_reclaimed() {
        // The property that separates tracing from reference counting. Two
        // objects referring to each other, dropped: a counting collector keeps
        // them forever and every other test here still passes.
        let allocations = allocations_beyond_trigger();
        let source = format!(
            "function main() {{ let i = 0; \
             while (i < {allocations}) {{ let a = {{}}; let b = {{}}; \
             a.peer = b; b.peer = a; i = i + 1; }} return 0; }} main();"
        );
        let program = compile(&source).expect("compiles");
        let mut runtime = Runtime::default();
        Vm::default()
            .run_function(
                &program,
                1,
                Vec::new(),
                &mut runtime,
                &mut NoHost::default(),
            )
            .expect("runs");

        assert!(
            runtime.heap.occupied_slots() < allocations,
            "{} slots occupied; unreachable cycles were retained",
            runtime.heap.occupied_slots()
        );
    }

    #[test]
    fn collection_leaves_no_roots_registered() {
        // Roots are registered per collection and cleared afterwards. A root
        // left behind keeps its object alive for the rest of the run, which
        // looks exactly like a collector that is merely conservative.
        let source = format!(
            "function main() {{ let kept = {{}}; let i = 0; \
             while (i < {}) {{ let junk = {{}}; i = i + 1; }} return 0; }} main();",
            allocations_beyond_trigger()
        );
        let program = compile(&source).expect("compiles");
        let mut runtime = Runtime::default();
        Vm::default()
            .run_function(
                &program,
                1,
                Vec::new(),
                &mut runtime,
                &mut NoHost::default(),
            )
            .expect("runs");

        assert!(
            runtime.heap.roots().is_empty(),
            "{} roots left registered after the run",
            runtime.heap.roots().len()
        );
    }
}
