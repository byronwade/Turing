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

/// A construct this implementation does not model, or a program error.
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum JsError {
    /// The lexer met a character it cannot start a token with.
    UnexpectedCharacter { character: char, offset: usize },
    /// The parser met a token it cannot use here.
    UnexpectedToken { found: String, expected: String },
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
            Self::Function(_) => true,
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
        if matches!(two, "==" | "!=" | "<=" | ">=" | "&&" | "||") {
            tokens.push(Token::Punct(two.to_string()));
            index += 2;
            continue;
        }
        if b"+-*/%<>=!(){};,".contains(&byte) {
            tokens.push(Token::Punct((byte as char).to_string()));
            index += 1;
            continue;
        }
        // Property access, arrays, and regular expressions all begin here.
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

struct Parser {
    tokens: Vec<Token>,
    position: usize,
}

impl Parser {
    const fn new(tokens: Vec<Token>) -> Self {
        Self {
            tokens,
            position: 0,
        }
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
        self.parse_assignment()
    }

    fn parse_assignment(&mut self) -> Result<Expr, JsError> {
        let target = self.parse_logical_or()?;
        if self.check_punct("=") {
            self.position += 1;
            let value = Box::new(self.parse_assignment()?);
            let Expr::Variable(name) = target else {
                return Err(JsError::UnexpectedToken {
                    found: "expression".to_string(),
                    expected: "a variable on the left of `=`".to_string(),
                });
            };
            return Ok(Expr::Assign { name, value });
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
        self.refuse_unsupported_keyword()?;
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
            Expr::Call { callee, arguments } => {
                let Some(&(_, index, arity)) =
                    self.signatures.iter().find(|(name, _, _)| name == callee)
                else {
                    return Err(JsError::UndefinedVariable {
                        name: callee.clone(),
                    });
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
}

impl Default for Vm {
    fn default() -> Self {
        Self {
            step_limit: 1_000_000,
        }
    }
}

impl Vm {
    /// Runs `program` and returns the top-level completion value.
    ///
    /// # Errors
    ///
    /// Returns [`JsError`] on a runtime type error or when the instruction
    /// budget is exhausted.
    pub fn run(&self, program: &Program) -> Result<Value, JsError> {
        let mut steps = 0_u64;
        self.run_function(program, 0, Vec::new(), &mut steps)
    }

    fn run_function(
        &self,
        program: &Program,
        index: usize,
        arguments: Vec<Value>,
        steps: &mut u64,
    ) -> Result<Value, JsError> {
        let function = &program.functions[index];
        let mut locals = vec![Value::Undefined; function.locals.max(arguments.len())];
        for (slot, argument) in arguments.into_iter().enumerate() {
            locals[slot] = argument;
        }
        let mut stack: Vec<Value> = Vec::new();
        let mut pointer = 0_usize;

        while pointer < function.code.len() {
            *steps += 1;
            if *steps > self.step_limit {
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
                            Value::String(format!("{left}{right}"))
                        }
                        _ => Value::Number(to_number(&left) + to_number(&right)),
                    };
                    stack.push(result);
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
                    let result = self.run_function(program, *index, arguments, steps)?;
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

fn to_number(value: &Value) -> f64 {
    match value {
        Value::Number(number) => *number,
        Value::Boolean(true) => 1.0,
        Value::Boolean(false) | Value::Null => 0.0,
        Value::String(text) => text.trim().parse::<f64>().unwrap_or(f64::NAN),
        Value::Undefined | Value::Function(_) => f64::NAN,
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

    /// Evaluates an expression by binding it and returning the binding.
    fn expr(source: &str) -> Value {
        let wrapped = format!("function main() {{ return {source}; }}");
        let program = compile(&format!("{wrapped} main();")).expect("compiles");
        // The top level's last value is discarded, so call directly.
        Vm::default()
            .run_function(&program, 1, Vec::new(), &mut 0)
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
                .run_function(&program, 1, Vec::new(), &mut 0)
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
                .run_function(&program, 1, Vec::new(), &mut 0)
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
                .run_function(&program, 1, Vec::new(), &mut 0)
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
                .run_function(&program, 2, Vec::new(), &mut 0)
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
                .run_function(&program, 2, Vec::new(), &mut 0)
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
                .run_function(&program, 1, Vec::new(), &mut 0)
                .expect("runs"),
            Value::Number(7.0)
        );
    }

    #[test]
    fn a_function_without_return_yields_undefined() {
        let program = compile("function f() { let a = 1; } f();").expect("compiles");
        assert_eq!(
            Vm::default()
                .run_function(&program, 1, Vec::new(), &mut 0)
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
                .run_function(&program, 1, Vec::new(), &mut 0)
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
        let vm = Vm { step_limit: 10_000 };
        let error = vm
            .run_function(&program, 1, Vec::new(), &mut 0)
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
                .run_function(&program, 1, Vec::new(), &mut 0)
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
}
