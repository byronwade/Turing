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
//! short-circuit evaluation, `if`/`else`, `while`, C-style `for`, prefix and
//! postfix `++`/`--`, compound assignment (`+=`, `-=`, `*=`, `/=`), blocks
//! with lexical scoping, function declarations, calls, recursion, `return`,
//! objects with property access, arrays with indexing and `length`, and
//! anonymous function *expressions* as first-class values with indirect
//! calls.
//!
//! `for (init; condition; update)` desugars to a block holding the init and a
//! `while`, so it needs no control-flow machinery beyond what `while` already
//! has, and its loop variable is scoped to the enclosing block like any other
//! `let`. `for...in` and `for...of` are not implemented and are refused as a
//! parse error rather than misread as the C-style form. `++`/`--`/`+=` etc.
//! desugar to ordinary assignment; incrementing anything but a plain variable
//! (a property, an arbitrary expression) is refused.
//!
//! A function expression captures enclosing **`const`** bindings by value —
//! a real closure for the safe case. Because a const cannot change, the
//! captured snapshot can never be observed to be wrong. Capturing a mutable
//! `let`/`var` is refused (by-reference cells are not built yet), as is
//! reaching more than one function level out; both are refusals, never a
//! silently-wrong captured value.
//!
//! Arrow functions — `x => x + 1`, `(a, b) => ...`, `() => { ... }` — are sugar
//! over the same function-value machinery and obey the same refuse-capture
//! boundary.
//!
//! Everything else returns a typed error rather than a partial evaluation:
//! by-reference capture of mutable bindings, multi-level capture, named
//! function expressions, `class`, `try`/`catch`, `async`/`await`, generators,
//! `eval`, array-literal and call-argument spread (object-literal spread,
//! `{...x}`, is implemented), and prototype semantics. Modules are not a
//! general feature either — `import`/`export` parse only the two narrow
//! forms real usage needs (see `parse_import_statement`), everything else
//! about them still refuses.
//!
//! Regular expressions are implemented, scoped to what real usage needs
//! rather than full ECMAScript regex syntax — see the [`regex`] module doc
//! comment for exactly what compiles and what is refused.
//!
//! The reason is sharper here than elsewhere in the engine. A partially
//! implemented language does not fail visibly; it computes a wrong value and
//! carries on. Refusing an unimplemented construct at compile time keeps every
//! program that *does* run trustworthy.
//!
//! # JSX
//!
//! JSX (`<Tag prop="a" other={b}>child1{child2}</Tag>`) is parsed and
//! desugared entirely at parse time into an ordinary call this crate already
//! knows how to compile — the same discipline the `for`-loop desugaring
//! above follows, applied to a syntax extension instead of a statement form.
//! This is **syntax only**: the desugared call names a function,
//! `__jsxCreateElement`, that this crate does not implement by default.
//! Calling it produces [`JsError::UnboundOperation`], exactly like calling
//! any other undeclared name — the correct, honest state until a host or
//! prelude binds that name to something (a real component/DOM runtime).
//! Parsing JSX and running it are different milestones, and this is only the
//! first.
//!
//! The name is `__jsxCreateElement`, not the more familiar `createElement`,
//! because this crate's own DOM host bindings already use the bare global
//! name `createElement` for a different, established operation (real DOM
//! node construction — see `turing-webidl`); giving JSX's desugar target a
//! distinct name avoids that collision entirely rather than depending on
//! call-site arity to disambiguate two unrelated operations sharing one name.
//!
//! `<Tag prop1="a" prop2={b}>child1{child2}</Tag>` desugars to
//! `__jsxCreateElement(Tag, {prop1: "a", prop2: b}, [child1, child2])`,
//! where:
//!
//! - The tag becomes the first argument. A lowercase-leading name (`<div>`)
//!   is a host/intrinsic element and passes as a **string**, `"div"`; an
//!   uppercase-leading name (`<Header>`) is a component reference and passes
//!   as the **identifier itself**, `Header` — an ordinary variable reference,
//!   evaluated and type-checked exactly like any other use of that name. This
//!   matches real JSX's own lowercase/uppercase convention and means an
//!   undeclared component fails to compile as [`JsError::UndefinedVariable`]
//!   rather than silently stringifying its name.
//! - Attributes become the second argument, an object literal built from
//!   them in source order (`{}` when there are none — always an object,
//!   never `null`, so the next phase never needs to null-check it).
//! - Children — text runs, `{expression}` children, and nested elements —
//!   become the third argument, an array literal built from them in source
//!   order (`[]` when there are none). Collected into one array, rather than
//!   passed as further variadic positional arguments, so every call site has
//!   the same fixed arity of three regardless of how many children a tag
//!   has — this compiler's calls (both to declared functions and to bound
//!   host operations) are checked against one fixed arity per name, which a
//!   variadic call site could not satisfy.
//! - A fragment, `<>child1<Foo /></>`, desugars the same way but names
//!   `Fragment` — a variable reference, the same convention a component
//!   uses — as the tag, with no attributes: `__jsxCreateElement(Fragment,
//!   {}, [child1, __jsxCreateElement(Foo, {}, [])])`.
//!
//! Supported: self-closing tags, tags with children, string (`x="a"`) and
//! `{expression}` attribute values (including an arrow function value, since
//! an attribute's brace content is parsed with the ordinary expression
//! grammar), text children, `{expression}` children, nested tags, mixed
//! text/element/expression children, and fragments. A text run that is pure
//! whitespace between tags contributes no child at all, so ordinarily
//! indented multi-line JSX does not produce spurious whitespace-only
//! arguments; a text run with any non-whitespace content is otherwise kept
//! verbatim, without JSX's fuller per-line trim-and-rejoin whitespace rule.
//!
//! Refused, each as a named [`JsError::Unsupported`] rather than a
//! misparse: spread attributes and spread children (`{...props}`), a
//! boolean-shorthand attribute (`<Foo disabled>` — write `disabled={true}`),
//! namespaced or hyphenated tag names (`<Foo.Bar>`), namespaced attribute
//! names, and an empty expression container (`{}`).
//!
//! JSX text and attribute values are not tokenized as JavaScript at all —
//! quoting and every other lexical rule this file's lexer applies simply do
//! not apply inside them — so they are scanned directly from the source
//! text rather than from the pre-lexed token stream, and ordinary
//! token-based parsing resumes at the first token starting at or after
//! where the scan ends. That handoff depends on JSX content staying within
//! the plain lexer's own character set; content that does not (most
//! plausibly an unescaped quote inside text, since this lexer has no escape
//! sequences) is refused rather than silently misaligning the tokens that
//! follow — seen in `Parser::resume_at`, which is the one place in this
//! feature where the limitation is checked rather than merely documented.

#![forbid(unsafe_code)]

use core::fmt;
use std::rc::Rc;
use turing_gc::{Bindings, GcRef, Heap, Trace};

mod regex;
pub use regex::CompiledRegex;

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
    /// An array. In this language an array *is* an object — a `length`
    /// property and integer-keyed elements — which is exactly the
    /// specification's model, so it shares the object heap and machinery and
    /// differs only in this tag, which selects array semantics for `length`
    /// maintenance and stringification.
    Array(GcRef),
    /// A closure: a function paired with the values it captured from an
    /// enclosing scope. The heap object holds the function index and the
    /// captured values; see `mod closure`. Only `const` bindings are
    /// captured, so the values are immutable snapshots.
    Closure(GcRef),
    /// A compiled regular expression.
    ///
    /// Reference-counted, not a `GcRef` into the collected heap: a
    /// `CompiledRegex` never refers to another `Value` (it is pure pattern
    /// data), so it cannot participate in a reference cycle, and never
    /// needs the tracing collector to find it — plain `Rc` counting is
    /// exact all by itself. A regex literal compiles its pattern exactly
    /// once, at `compile()` time; every execution of that literal (however
    /// many times it runs — inside a loop, inside a repeatedly-called
    /// function) clones this `Rc`, which is a pointer copy and a refcount
    /// bump, not a recompile. See `mod regex`.
    Regex(Rc<regex::CompiledRegex>),
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
            // Every object is truthy, including an empty one, and an array is
            // an object — even an empty array is truthy, the classic trap.
            // A regex value is likewise always truthy, real JS's own rule.
            Self::Function(_) | Self::Object(_) | Self::Array(_) | Self::Closure(_) => true,
            Self::Regex(_) => true,
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
            // Array-to-string joins elements with commas, which needs to read
            // the heap this infallible formatter cannot reach. Rather than
            // print a wrong value, it prints a marker; a caller that needs the
            // joined form uses the element access that does have the heap.
            Self::Array(_) => write!(formatter, "[object Array]"),
            // A closure stringifies like any function.
            Self::Closure(_) => write!(formatter, "[function]"),
            Self::Regex(regex) => write!(formatter, "/{}/{}", regex.source, regex.flags),
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
    /// A backtick template literal, already split into its literal text
    /// runs and the raw source text of each `${...}` interpolation. The
    /// interpolations are not parsed here — the lexer has no AST to build
    /// them into — that happens in `parse_primary`, by recursively lexing
    /// and parsing each one as an ordinary expression.
    TemplateLiteral(Vec<TemplatePart>),
    /// A `/pattern/flags` regular-expression literal, pattern and flags
    /// already split apart. See `regex_may_start_here` for how the lexer
    /// tells this apart from the division operator, and `mod regex` for
    /// what patterns this engine actually compiles.
    Regex(String, String),
    Eof,
}

/// One piece of a template literal.
#[derive(Clone, Debug, Eq, PartialEq)]
enum TemplatePart {
    /// A literal text run, exactly as written (no escape processing — this
    /// codebase's plain string literals do not process escapes either, so
    /// this matches, not falls short of, that existing precedent).
    Str(String),
    /// The raw, unparsed source text of a `${...}` interpolation's
    /// expression, not including the `${`/`}` delimiters.
    Expr(String),
}

impl Token {
    fn describe(&self) -> String {
        match self {
            Self::Number(text)
            | Self::Str(text)
            | Self::Ident(text)
            | Self::Keyword(text)
            | Self::Punct(text) => format!("`{text}`"),
            Self::TemplateLiteral(_) => "a template literal".to_string(),
            Self::Regex(pattern, flags) => format!("`/{pattern}/{flags}`"),
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
///
/// `delete` is deliberately absent — like `typeof`, it is a real,
/// implemented (if scoped) feature now, not a blanket refusal, and this
/// table's lookup fires at the very start of `parse_statement_inner` too,
/// before any expression parsing runs. Real Nova usage is always a bare
/// `delete object.key;` statement, not an assignment or a return value, so
/// that early check would refuse it before `Parser::parse_unary_inner`'s
/// own, more specific handling ever ran. `typeof`'s explicit refusal inside
/// `parse_unary_inner` is unaffected by that same statement-level check for
/// the identical reason — it, too, is not in this table.
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
    ("instanceof", "instanceof"),
    ("switch", "switch"),
    ("do", "do/while"),
];

/// Native modules this engine provides bindings for, via whatever prelude
/// the embedder supplies as ordinary top-level declarations — not a real
/// module resolver. See `Parser::parse_import_statement`.
const NATIVE_MODULES: &[&str] = &["react", "lucide-react"];

/// Lexes `source`, returning each token alongside the byte offset its first
/// character starts at (`Token::Eof`'s offset is `source.len()`).
///
/// The offsets exist for JSX (see the module-level doc comment on JSX): JSX
/// text is not JavaScript and is scanned directly from these same source
/// bytes rather than through this token stream, and the offsets are how the
/// parser finds, after such a scan, which pre-lexed token to resume from.
///
/// `tolerate_unknown` governs what happens when a byte reaches the fallback
/// at the bottom of the scan loop — one that starts no known token. `true`
/// (only from [`compile`], lexing the *whole file* once, eagerly) skips it
/// rather than erroring: this pass's only job over a JSX region is to leave
/// *some* token stream for JSX's own raw-byte re-scan to resynchronize
/// with afterward (see the module-level JSX doc comment and
/// `Parser::resume_at`) — its tokenization of that region is discarded
/// once that direct scan runs, so a byte with no ordinary-JS meaning
/// (`&` from `Wade's Plumbing &amp; Septic LLC`'s literal JSX text, or any
/// non-ASCII byte — Nova writes curly quotes, emoji, Japanese titles
/// directly and unquoted) is safe to skip rather than fail the whole
/// compile over.
///
/// `false` (from [`parse_expression_from_source`] and
/// [`Parser::parse_embedded_expression`], each re-lexing a substring that
/// is already known to be real code — a template-literal interpolation or
/// a JSX `{expr}`) keeps the strict, error-on-unknown-byte behavior:
/// unlike the eager whole-file pass, this token stream *is* what compiles,
/// not a discarded placeholder. Tolerating an unknown byte here would
/// silently drop it from the token stream instead of refusing — exactly
/// the never-silently-wrong violation this crate's entire error-handling
/// discipline exists to prevent. Concretely: Nova's `rgba(${(n >> 16) &
/// 255}, ...)` uses the bitwise `&` operator, which this engine does not
/// implement, inside a template interpolation — that `&` never reaches
/// the eager pass at all (`scan_template_literal` brace-skips over
/// interpolation bodies without lexing their contents), but it does reach
/// this strict re-lex once parsing actually resolves the interpolation,
/// and must refuse there rather than vanish.
fn lex(source: &str, tolerate_unknown: bool) -> Result<(Vec<Token>, Vec<usize>), JsError> {
    let bytes = source.as_bytes();
    let mut tokens = Vec::new();
    let mut starts = Vec::new();
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
            starts.push(start);
            tokens.push(Token::Number(source[start..index].to_string()));
            continue;
        }
        if byte == b'"' || byte == b'\'' {
            let token_start = index;
            let quote = byte;
            index += 1;
            let start = index;
            while index < bytes.len() && bytes[index] != quote && bytes[index] != b'\n' {
                index += 1;
            }
            // A real JS string literal can never contain a raw newline, so
            // hitting one before the closing quote proves this was never a
            // string open at all — e.g. an apostrophe written directly in
            // unquoted JSX text ("...only what's on screen exists...").
            // Every genuine single-quoted/double-quoted literal in the real
            // Nova file is a single line (verified by simulating this exact
            // scan over the whole file and checking for newline-crossings
            // before shipping this), so this is a grammar fact, not a
            // tuned heuristic. Without it, the bogus "string" this quote
            // opened would keep scanning past the newline until some later,
            // unrelated quote character happened to close it — corrupting
            // every real token in between (confirmed: one apostrophe near
            // real-file byte 323116 previously swallowed ~25KB this way).
            if index >= bytes.len() || bytes[index] == b'\n' {
                if tolerate_unknown {
                    // This pass's tokenization of a JSX-text region is
                    // discarded once JSX's own raw-byte re-scan takes over
                    // (see `tolerate_unknown`'s doc comment) — resume right
                    // after the stray quote byte, same as any other
                    // unrecognized byte, rather than treating it as an
                    // unterminated string.
                    index = token_start + 1;
                    continue;
                }
                return Err(JsError::UnexpectedCharacter {
                    character: quote as char,
                    offset: token_start,
                });
            }
            starts.push(token_start);
            tokens.push(Token::Str(source[start..index].to_string()));
            index += 1;
            continue;
        }
        if byte == b'`' {
            let token_start = index;
            let (parts, next) = scan_template_literal(source, index + 1)?;
            starts.push(token_start);
            tokens.push(Token::TemplateLiteral(parts));
            index = next;
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
            starts.push(start);
            if KEYWORDS.contains(&word) {
                tokens.push(Token::Keyword(word.to_string()));
            } else {
                tokens.push(Token::Ident(word.to_string()));
            }
            continue;
        }
        // A `/` starts a regex literal rather than the division operator
        // when the previous token could not itself have ended an
        // expression — see `regex_may_start_here`. Checked ahead of the
        // two-/three-character operator matches below so `/=` inside a
        // regex body (e.g. `/=foo/`) is scanned as pattern text, not
        // mis-lexed as the compound-assignment operator.
        if byte == b'/' && regex_may_start_here(tokens.last()) {
            let token_start = index;
            let (pattern, flags, next) = scan_regex_literal(source, index + 1)?;
            starts.push(token_start);
            tokens.push(Token::Regex(pattern, flags));
            index = next;
            continue;
        }
        // Multi-character operators are matched longest-first so that `===`
        // does not lex as `==` followed by `=`.
        let three = source.get(index..index + 3).unwrap_or("");
        let two = source.get(index..index + 2).unwrap_or("");
        if matches!(three, "===" | "!==") {
            starts.push(index);
            tokens.push(Token::Punct(three.to_string()));
            index += 3;
            continue;
        }
        // `...` before `.`, so spread lexes as one token and can be refused
        // as itself rather than as three property accesses.
        if three == "..." {
            starts.push(index);
            tokens.push(Token::Punct(three.to_string()));
            index += 3;
            continue;
        }
        if matches!(
            two,
            "==" | "!="
                | "<="
                | ">="
                | "&&"
                | "||"
                | "=>"
                | "++"
                | "--"
                | "+="
                | "-="
                | "*="
                | "/="
        ) {
            starts.push(index);
            tokens.push(Token::Punct(two.to_string()));
            index += 2;
            continue;
        }
        if b"+-*/%<>=!(){};,.[]:?".contains(&byte) {
            starts.push(index);
            tokens.push(Token::Punct((byte as char).to_string()));
            index += 1;
            continue;
        }
        // A non-ASCII byte reaching here is never inside a string/template
        // literal or a comment — both already scan raw bytes to their own
        // closing delimiter above, with no interest in what those bytes
        // are — so a byte reaching here, in the eager whole-file pass, can
        // only be one of two things: a Unicode character written directly
        // as JSX text (Nova does this constantly — curly quotes, emoji,
        // ⌘, Japanese titles in its own fixture data — all outside any
        // quote), or an ASCII byte with no meaning in this engine's
        // (deliberately small) operator set written the same way — `&`
        // from a literal `&amp;`/`&nbsp;` or a bare "Cookies & site data"
        // in JSX text is the real example that motivated this. See this
        // function's own doc comment on `tolerate_unknown` for why
        // skipping is safe here specifically (this pass's tokenization of
        // a JSX region is discarded once JSX's own raw-byte re-scan runs)
        // and not safe in the two substring re-lex call sites, which keep
        // the strict, error-on-unknown-byte behavior below instead.
        // Skipping one byte at a time is safe regardless of a multi-byte
        // UTF-8 sequence's length, since every continuation byte is also
        // >= 0x80 and takes this same path in turn.
        if tolerate_unknown {
            index += 1;
            continue;
        }
        return Err(JsError::UnexpectedCharacter {
            character: byte as char,
            offset: index,
        });
    }
    starts.push(bytes.len());
    tokens.push(Token::Eof);
    Ok((tokens, starts))
}

/// Whether a `/` at the current lex position opens a regex literal rather
/// than meaning division or compound-assignment-by-division.
///
/// The standard rule real JS lexers use, and the one this one follows: `/`
/// is division only when the previous token could itself have been the
/// end of a value-producing expression (a literal, an identifier, `)`
/// closing a call/parenthesised expression, `]` closing an index, or
/// `++`/`--` as a postfix operator). After anything else — an operator, an
/// opening bracket, `return`, a keyword like `typeof` that is always
/// followed by an operand, or the very start of input — a `/` can only be
/// opening a new expression, so it starts a regex.
///
/// This is genuinely ambiguous in general JS grammar only after `)`, which
/// closes either a parenthesised *expression* (`(a) / b`, division) or an
/// `if`/`while`/`for` *header* (`if (x) /re/.test(y)`, division is not
/// even meaningful there) — a real engine disambiguates by tracking
/// grammatical context, not just the previous token. This lexer does not:
/// it treats `)` as always ending an expression, i.e. always division.
/// Nova's own 25 real regex literals never follow `)` (confirmed by
/// inspection before this was written; see the
/// `turing-nova-source-real-scope` project memory), so this simpler rule
/// is correct for every pattern that actually needs to compile, and the
/// gap is a known, accepted limitation rather than a silent one.
///
/// `<` and `}` get the same "always division" treatment for a different,
/// JSX-specific reason: this whole-file eager lex pass runs before any
/// JSX-aware re-scanning (see the module-level JSX doc comment), so it
/// tokenizes JSX syntax as if it were plain JS, with no idea it is inside
/// a tag. That makes two JSX constructs land here as `/` right after one
/// of these punctuators, indistinguishable at this point from ordinary JS:
/// a closing tag's `</` (`Punct("<")` then `/`), and a self-closing tag's
/// `/>` right after an attribute expression brace or spread —
/// `<Foo prop={expr} />` and `<Foo {...props} />` both tokenize their `/>`
/// as `Punct("}")` then `/`. Real JS regex literals essentially never
/// follow `<` or `}` (comparing a value to a regex object, or a regex
/// statement bare after a block, are not meaningful patterns), while both
/// JSX shapes above are common, so treating `<`/`}` as always ending an
/// expression — division, never a regex start — is correct for real usage
/// and avoids the eager pass mis-scanning a tag as an unterminated regex.
fn regex_may_start_here(previous: Option<&Token>) -> bool {
    match previous {
        None => true,
        Some(
            Token::Number(_)
            | Token::Str(_)
            | Token::Ident(_)
            | Token::TemplateLiteral(_)
            | Token::Regex(_, _),
        ) => false,
        // `this`/`true`/`false`/`null`/`undefined` are values, ending an
        // expression like any other literal; every other keyword (`return`,
        // `typeof`, `new`, etc.) is always followed by an operand.
        Some(Token::Keyword(word)) => !matches!(
            word.as_str(),
            "this" | "true" | "false" | "null" | "undefined"
        ),
        // `)` and `]` close a value-producing expression (division); `++`/
        // `--` here are the postfix form, also closing one; `<`/`}` are the
        // JSX-tag cases explained above. Every other punctuator —
        // including `(`, `[`, `{`, `,`, `;`, `:`, `?`, and every other
        // binary/logical/assignment operator — is always followed by an
        // operand.
        Some(Token::Punct(text)) => !matches!(text.as_str(), ")" | "]" | "++" | "--" | "<" | "}"),
        Some(Token::Eof) => true,
    }
}

/// Scans a regex literal's body, `index` positioned just past the opening
/// `/`. Returns the pattern text, the flag letters, and the index just
/// past the last flag letter.
///
/// A `\` escapes the next character (including `/`), and an unescaped `[`
/// opens a character class inside which an unescaped `/` does not close
/// the literal — both mirror how `/` is actually allowed to appear inside
/// a pattern's own body. A `]` that would close a class immediately after
/// `[` or `[^` (a literal `]` by the ECMAScript grammar) is not treated
/// specially, since no real usage relies on it.
fn scan_regex_literal(source: &str, mut index: usize) -> Result<(String, String, usize), JsError> {
    let opening_slash = index - 1;
    let bytes = source.as_bytes();
    let pattern_start = index;
    let mut in_class = false;
    loop {
        if index >= bytes.len() || bytes[index] == b'\n' {
            return Err(JsError::UnexpectedToken {
                found: "end of input".to_string(),
                expected: format!(
                    "a closing `/` for the regular-expression literal starting at byte {opening_slash}"
                ),
            });
        }
        match bytes[index] {
            b'\\' => index += 2,
            b'[' => {
                in_class = true;
                index += 1;
            }
            b']' => {
                in_class = false;
                index += 1;
            }
            b'/' if !in_class => break,
            _ => index += 1,
        }
    }
    let pattern = source[pattern_start..index].to_string();
    index += 1; // closing '/'
    let flags_start = index;
    while index < bytes.len() && bytes[index].is_ascii_alphabetic() {
        index += 1;
    }
    let flags = source[flags_start..index].to_string();
    Ok((pattern, flags, index))
}

/// Scans a template literal's body, `index` positioned just past the
/// opening backtick. Returns the parts and the index just past the
/// closing backtick.
///
/// Interpolations are found by brace-depth counting, skipping over nested
/// `"`/`'` string literals so a `}` inside one does not end the
/// interpolation early — mirroring the plain-string scan above, which
/// likewise does no escape processing (neither needs to, since this
/// language's string literals have none). A nested template literal
/// inside an interpolation is refused rather than handled, to avoid the
/// much harder problem of properly nested recursive scanning; no real
/// Nova usage needs it.
fn scan_template_literal(
    source: &str,
    mut index: usize,
) -> Result<(Vec<TemplatePart>, usize), JsError> {
    let opening_backtick = index - 1;
    let bytes = source.as_bytes();
    let mut parts = Vec::new();
    let mut text_start = index;
    loop {
        if index >= bytes.len() {
            return Err(JsError::UnexpectedToken {
                found: "end of input".to_string(),
                expected: format!(
                    "a closing backtick for the template literal starting at byte {opening_backtick}"
                ),
            });
        }
        match bytes[index] {
            b'`' => {
                parts.push(TemplatePart::Str(source[text_start..index].to_string()));
                return Ok((parts, index + 1));
            }
            b'$' if bytes.get(index + 1) == Some(&b'{') => {
                parts.push(TemplatePart::Str(source[text_start..index].to_string()));
                index += 2;
                let expr_start = index;
                let mut depth = 1usize;
                while depth > 0 {
                    if index >= bytes.len() {
                        return Err(JsError::UnexpectedToken {
                            found: "end of input".to_string(),
                            expected: format!(
                                "a closing `}}` for the template interpolation starting at byte {expr_start}"
                            ),
                        });
                    }
                    match bytes[index] {
                        b'`' => {
                            return Err(JsError::Unsupported {
                                feature: "nested template literals".to_string(),
                            });
                        }
                        b'"' | b'\'' => {
                            let quote = bytes[index];
                            index += 1;
                            while index < bytes.len() && bytes[index] != quote {
                                index += 1;
                            }
                        }
                        b'{' => depth += 1,
                        b'}' => depth -= 1,
                        _ => {}
                    }
                    if depth > 0 {
                        index += 1;
                    }
                }
                parts.push(TemplatePart::Expr(source[expr_start..index].to_string()));
                index += 1;
                text_start = index;
            }
            _ => index += 1,
        }
    }
}

// -- ast -----------------------------------------------------------------

#[derive(Clone, Debug, PartialEq)]
enum Expr {
    Number(f64),
    Str(String),
    Boolean(bool),
    Null,
    Undefined,
    /// A `/pattern/flags` literal. Compiled to a matcher once, at compile
    /// time — see `Compiler::expression`'s `Expr::Regex` arm and `mod
    /// regex`.
    Regex {
        pattern: String,
        flags: String,
    },
    /// `new RegExp(pattern)` / `new RegExp(pattern, flags)`, the one
    /// `new`-expression this engine implements (see `Parser::parse_new`).
    /// Unlike `Expr::Regex`, the pattern is an arbitrary runtime
    /// expression, not fixed source text, so it compiles the pattern at
    /// runtime rather than once here.
    NewRegExp {
        arguments: Vec<Expr>,
    },
    Variable(String),
    Unary {
        operator: String,
        operand: Box<Expr>,
    },
    /// `delete object.key` / `delete object[key]`. Scoped to exactly that
    /// shape — real Nova usage never targets a bare variable or anything
    /// else `delete` can grammatically apply to — refused rather than
    /// mishandled at parse time by `Parser::parse_unary_inner`, which only
    /// builds this node when its operand is already an `Expr::Member`.
    Delete {
        object: Box<Expr>,
        key: Box<Expr>,
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
    /// A call whose callee is an arbitrary expression evaluating to a function
    /// value: `arr[0]()`, `(f)()`, `obj.m()` once methods exist.
    CallValue {
        callee: Box<Expr>,
        arguments: Vec<Expr>,
    },
    /// An anonymous function expression, `function(params) { body }`. It
    /// evaluates to a function value. It does not capture enclosing locals —
    /// a reference to one is refused at compile time as undefined rather than
    /// captured — so it is a first-class value, not yet a closure.
    ///
    /// `min_arity` is the count of leading parameters with no default value
    /// (`parameters.len()` when none has one) — see [`Function::min_arity`]'s
    /// doc comment for how it relaxes the call-site arity check.
    Lambda {
        parameters: Vec<String>,
        body: Vec<Stmt>,
        min_arity: usize,
    },
    /// Postfix `x++` / `x--`: assigns `x + delta` but evaluates to the old
    /// value of `x`.
    PostUpdate {
        name: String,
        delta: f64,
    },
    /// Compound assignment to a property, `object[key] op= right` /
    /// `object.key op= right`. A dedicated node rather than desugaring to
    /// `SetMember { value: Binary { Member { object, key }, right } } }` at
    /// parse time: that desugaring would compile `object` and `key` twice —
    /// once for the write target, once inside the read of the current value
    /// — silently re-running any side effect they contain (a call as the
    /// object, a call as a computed key) an extra time. The specification
    /// evaluates the base reference once; this node compiles that way.
    CompoundMember {
        object: Box<Expr>,
        key: Box<Expr>,
        operator: String,
        right: Box<Expr>,
    },
    /// `{ a: 1, ...rest, "b": 2 }`, in source order.
    ObjectLiteral {
        entries: Vec<ObjectEntry>,
    },
    /// `[a, b, c]`, in source order.
    ArrayLiteral {
        elements: Vec<Expr>,
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
    /// `condition ? then_branch : else_branch`. Only the taken branch is
    /// compiled to run — the untaken one must not evaluate, the same
    /// short-circuit contract `Expr::Logical` already keeps for `&&`/`||`.
    Conditional {
        condition: Box<Expr>,
        then_branch: Box<Expr>,
        else_branch: Box<Expr>,
    },
    /// `object.name(arguments)` — a dedicated node (like `CompoundMember`)
    /// so `object` compiles exactly once. Resolved entirely at runtime: an
    /// own property of `object` named `name` that holds a function or
    /// closure is called normally, exactly the existing indirect-call path
    /// (so a callback prop that happens to be named e.g. `filter` is not
    /// shadowed by anything here); only when no such own property exists
    /// does a String or Array receiver fall back to one of a fixed set of
    /// built-in methods, refusing with a typed error for anything neither
    /// path recognises.
    MethodCall {
        object: Box<Expr>,
        name: String,
        arguments: Vec<Expr>,
    },
}

/// One entry of an object literal.
#[derive(Clone, Debug, PartialEq)]
enum ObjectEntry {
    /// `key: value`.
    Property(String, Expr),
    /// `...expr` — copies every own property of the evaluated value onto
    /// the object under construction. `null`/`undefined` spread nothing
    /// (matching real JS); any other non-object/array value refuses rather
    /// than silently spreading nothing, since that could hide a real
    /// mistake (e.g. spreading a string, which real JS would spread as
    /// per-index characters — a case this engine does not model) instead
    /// of matching a genuine no-op case.
    Spread(Expr),
}

#[derive(Clone, Debug, PartialEq)]
enum Stmt {
    Declare {
        name: String,
        value: Option<Expr>,
        constant: bool,
    },
    /// Several statements compiled in place, in the *current* scope rather
    /// than a fresh one — unlike [`Stmt::Block`], which is a real block
    /// scope. Exists for destructuring: `const [a, b] = pair;` binds `a` and
    /// `b` into the scope the `const` itself is in, not a scope that
    /// disappears the moment the desugared statements finish running.
    Sequence(Vec<Stmt>),
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
        min_arity: usize,
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

/// One array-pattern slot: `None` for an elided hole (`[a, , b]`'s middle
/// element), `Some((name, default))` for a bound name and its optional
/// default expression.
type ArrayPatternBindings = Vec<Option<(String, Option<Expr>)>>;

/// One object-pattern property: `(source_key, binding_name, default)` — for
/// shorthand `{a}`, `source_key == binding_name`; for a rename `{a: b}`,
/// they differ.
type ObjectPatternBindings = Vec<(String, String, Option<Expr>)>;

/// Desugars an array destructuring pattern into a temp declaration plus one
/// declaration per binding — see [`Stmt::Sequence`]'s doc comment for why
/// this must not become a `Stmt::Block`. `value` is compiled exactly once,
/// into `temp`, regardless of how many bindings read from it or whether any
/// carries a default; an elided slot (`None`) binds nothing at all.
fn desugar_array_pattern(
    bindings: ArrayPatternBindings,
    value: Expr,
    constant: bool,
    temp: String,
) -> Vec<Stmt> {
    let mut statements = vec![Stmt::Declare {
        name: temp.clone(),
        value: Some(value),
        constant: true,
    }];
    for (index, binding) in bindings.into_iter().enumerate() {
        let Some((name, default)) = binding else {
            continue;
        };
        let read = Expr::Member {
            object: Box::new(Expr::Variable(temp.clone())),
            key: Box::new(Expr::Number(index as f64)),
        };
        statements.push(Stmt::Declare {
            name,
            value: Some(apply_pattern_default(read, default)),
            constant,
        });
    }
    statements
}

/// Desugars an object destructuring pattern the same way
/// [`desugar_array_pattern`] does, reading each binding by its source
/// property name instead of by index.
fn desugar_object_pattern(
    bindings: ObjectPatternBindings,
    value: Expr,
    constant: bool,
    temp: String,
) -> Vec<Stmt> {
    let mut statements = vec![Stmt::Declare {
        name: temp.clone(),
        value: Some(value),
        constant: true,
    }];
    for (key, name, default) in bindings {
        let read = Expr::Member {
            object: Box::new(Expr::Variable(temp.clone())),
            key: Box::new(Expr::Str(key)),
        };
        statements.push(Stmt::Declare {
            name,
            value: Some(apply_pattern_default(read, default)),
            constant,
        });
    }
    statements
}

/// `read` unchanged when `default` is absent; otherwise
/// `read === undefined ? default : read` — real destructuring-default
/// semantics, where only a genuinely `undefined` value falls back, not a
/// falsy-but-present one like `0`, `""`, or `false` (`zoom = 1` must not
/// override an explicitly passed `zoom: 0`). `read` has no side effects of
/// its own — it is always a plain variable indexed by a compile-time
/// constant — so compiling it twice here costs nothing but is never wrong.
fn apply_pattern_default(read: Expr, default: Option<Expr>) -> Expr {
    match default {
        None => read,
        Some(default_expr) => Expr::Conditional {
            condition: Box::new(Expr::Binary {
                operator: "===".to_string(),
                left: Box::new(read.clone()),
                right: Box::new(Expr::Undefined),
            }),
            then_branch: Box::new(default_expr),
            else_branch: Box::new(read),
        },
    }
}

/// Formats an arity-mismatch error's argument-count description: `"3"` when
/// `min == max` (no default parameters, the ordinary case), `"3 to 4"`
/// otherwise — used at both the compile-time named-call check and the
/// runtime function-value call check, so a caller sees the same wording
/// either way.
fn arity_range(min_arity: usize, arity: usize) -> String {
    if min_arity == arity {
        arity.to_string()
    } else {
        format!("{min_arity} to {arity}")
    }
}

struct Parser<'a> {
    tokens: Vec<Token>,
    /// Byte offset each token in `tokens` starts at, same length and index
    /// alignment as `tokens`. Unused by ordinary token-based parsing; it
    /// exists for JSX, which parses a run of the underlying source directly
    /// (see the module-level doc comment on JSX) and uses these to find
    /// where to resume afterward.
    starts: Vec<usize>,
    /// The original source, for JSX's raw-source scanning.
    source: &'a str,
    position: usize,
    /// Current recursion depth, bounded by [`MAX_NESTING_DEPTH`].
    depth: usize,
    /// Bumped once per destructuring pattern parsed, so the temporary
    /// binding a pattern desugars through (`__pattern0`, `__pattern1`, ...)
    /// is unique per occurrence rather than one name reused and shadowed
    /// throughout the whole program.
    pattern_count: usize,
}

impl<'a> Parser<'a> {
    const fn new(source: &'a str, tokens: Vec<Token>, starts: Vec<usize>) -> Self {
        Self {
            tokens,
            starts,
            source,
            position: 0,
            depth: 0,
            pattern_count: 0,
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

        if self.check_keyword("import") {
            return self.parse_import_statement();
        }
        if self.check_keyword("export") {
            return self.parse_export_statement();
        }
        if self.check_keyword("function") {
            return self.parse_function();
        }
        if self.check_keyword("var") || self.check_keyword("let") || self.check_keyword("const") {
            let Token::Keyword(kind) = self.advance() else {
                unreachable!("checked above")
            };
            let constant = kind == "const";
            if self.check_punct("[") || self.check_punct("{") {
                let statements = self.parse_destructuring_declaration(constant)?;
                self.eat_punct(";");
                return Ok(Stmt::Sequence(statements));
            }
            // `const a = 1, b = 2;` — real Nova usage (e.g. `const
            // DESIGN_W = 1440, DESIGN_H = 900;`) declares several bindings
            // in one statement. Each declarator desugars to its own
            // `Stmt::Declare`; more than one is wrapped in a
            // `Stmt::Sequence` (same-scope, not [`Stmt::Block`]'s fresh
            // scope — see its doc comment) so every name lands in the
            // enclosing scope exactly as if each had been written as its
            // own `const`/`let`/`var` statement. A single declarator stays
            // a bare `Stmt::Declare`, unchanged from before this supported
            // more than one.
            //
            // Correct only because this engine has no comma/sequence
            // operator: every `,` that is not a declarator separator sits
            // inside a `(`/`[`/`{` a nested parser already consumes whole
            // (e.g. `const a = f(1, 2), b = 3;`), so `parse_expression`
            // always stops exactly at the separator. If a comma operator
            // is ever added, a bare `const a = (x, y), b;` would need this
            // loop revisited.
            let mut declarations = Vec::new();
            loop {
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
                declarations.push(Stmt::Declare {
                    name,
                    value,
                    constant,
                });
                if !self.eat_punct(",") {
                    break;
                }
            }
            self.eat_punct(";");
            return Ok(if declarations.len() == 1 {
                declarations.into_iter().next().expect("checked len == 1")
            } else {
                Stmt::Sequence(declarations)
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
        if self.check_keyword("for") {
            return self.parse_for();
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
        let (parameters, prelude, min_arity) = self.parse_parameter_list()?;
        self.expect_punct("{")?;
        let mut body = prelude;
        while !self.check_punct("}") && !matches!(self.peek(), Token::Eof) {
            body.push(self.parse_statement()?);
        }
        self.expect_punct("}")?;
        Ok(Stmt::Function {
            name,
            parameters,
            body,
            min_arity,
        })
    }

    /// Parses `import Default, { Name (as Alias)?, ... } from "module";` —
    /// either half of the binding list may be absent, but at least one
    /// must be present. Two other forms are recognized only to refuse
    /// them explicitly (`import * as ns from "..."` and a bare
    /// `import "...";` for side effects) rather than falling through to a
    /// confusing later error. Real ES modules resolve arbitrary paths to
    /// arbitrary exports; this only recognizes a fixed whitelist of
    /// module names this engine itself provides native bindings for (see
    /// `NATIVE_MODULES`) — anything else refuses immediately, a far
    /// clearer error than letting an unresolved name fail later at first
    /// use.
    ///
    /// Compiles to nothing for a non-aliased named import: the embedder's
    /// prelude already declares that exact top-level name as an ordinary
    /// global (the same mechanism `memo`/`__jsxCreateElement` already use
    /// in `turing-engine`'s examples), so there is nothing left to bind.
    /// An aliased import (`Original as Alias`) is the one case that needs
    /// a *new* binding, and desugars to `const Alias = Original;` —
    /// referencing the prelude's existing `Original` global to create the
    /// distinct `Alias` name the importing code actually uses. The
    /// default binding (`import React from "react"`) is parsed but never
    /// bound to anything: no real Nova usage references it as a value
    /// (confirmed by direct grep against the pinned source), so binding
    /// it to a real namespace object is deferred until something actually
    /// needs it — a real, visible gap (a future reference fails as
    /// `UndefinedVariable`), not a value silently routed around.
    fn parse_import_statement(&mut self) -> Result<Stmt, JsError> {
        self.position += 1; // `import`
        if self.check_punct("*") {
            return Err(JsError::Unsupported {
                feature: "`import * as name` namespace imports".to_string(),
            });
        }
        if matches!(self.peek(), Token::Str(_)) {
            return Err(JsError::Unsupported {
                feature: "side-effect-only imports (`import \"module\";`)".to_string(),
            });
        }
        let mut has_default = false;
        if let Token::Ident(_) = self.peek() {
            self.advance(); // the default binding name — parsed, never bound
            has_default = true;
            self.eat_punct(",");
        }
        let mut aliases: Vec<(String, String)> = Vec::new();
        if self.eat_punct("{") {
            while !self.check_punct("}") {
                let original = match self.advance() {
                    Token::Ident(name) => name,
                    other => {
                        return Err(JsError::UnexpectedToken {
                            found: other.describe(),
                            expected: "an imported name".to_string(),
                        });
                    }
                };
                let local = if matches!(self.peek(), Token::Ident(word) if word == "as") {
                    self.advance();
                    match self.advance() {
                        Token::Ident(name) => name,
                        other => {
                            return Err(JsError::UnexpectedToken {
                                found: other.describe(),
                                expected: "a local binding name after `as`".to_string(),
                            });
                        }
                    }
                } else {
                    original.clone()
                };
                if local != original {
                    aliases.push((original, local));
                }
                if !self.eat_punct(",") {
                    break;
                }
            }
            self.expect_punct("}")?;
        } else if !has_default {
            return Err(JsError::UnexpectedToken {
                found: self.peek().describe(),
                expected: "a default binding, a `{ ... }` named-import list, or both".to_string(),
            });
        }
        if !matches!(self.peek(), Token::Ident(word) if word == "from") {
            return Err(JsError::UnexpectedToken {
                found: self.peek().describe(),
                expected: "`from`".to_string(),
            });
        }
        self.advance();
        let module = match self.advance() {
            Token::Str(text) => text,
            other => {
                return Err(JsError::UnexpectedToken {
                    found: other.describe(),
                    expected: "a module name string".to_string(),
                });
            }
        };
        if !NATIVE_MODULES.contains(&module.as_str()) {
            return Err(JsError::Unsupported {
                feature: format!("importing from \"{module}\" (no native binding for this module)"),
            });
        }
        self.eat_punct(";");
        let statements = aliases
            .into_iter()
            .map(|(original, local)| Stmt::Declare {
                name: local,
                value: Some(Expr::Variable(original)),
                constant: true,
            })
            .collect();
        Ok(Stmt::Sequence(statements))
    }

    /// Parses `export default function Name(...) { ... }` — the only
    /// export form real Nova usage needs (confirmed by direct grep: it is
    /// the file's sole `export`). `export`/`default` carry no meaning
    /// without a real module system to export *to*; they are consumed
    /// and discarded, and the function declaration underneath compiles
    /// exactly as an ordinary top-level `function` would. Any other
    /// export form (named exports, `export const`, `export default` of a
    /// non-function expression) refuses rather than guessing what it
    /// should do.
    fn parse_export_statement(&mut self) -> Result<Stmt, JsError> {
        self.position += 1; // `export`
        if !matches!(self.peek(), Token::Ident(word) if word == "default") {
            return Err(JsError::Unsupported {
                feature: "named exports (`export { ... }`, `export const ...`)".to_string(),
            });
        }
        self.advance(); // `default`
        if !self.check_keyword("function") {
            return Err(JsError::Unsupported {
                feature: "`export default` of anything but a function declaration".to_string(),
            });
        }
        self.parse_function()
    }

    fn parse_expression(&mut self) -> Result<Expr, JsError> {
        self.enter()?;
        let expression = self.parse_assignment();
        self.leave();
        expression
    }

    fn parse_assignment(&mut self) -> Result<Expr, JsError> {
        if self.arrow_ahead() {
            return self.parse_arrow();
        }
        let target = self.parse_logical_or()?;
        if self.eat_punct("?") {
            // Right-associative: the branches recurse into `parse_assignment`
            // (not back into the ternary's own precedence level), so a chain
            // like `a ? b : c ? d : e` reads as `a ? b : (c ? d : e)`, and
            // each branch may itself be an assignment or another ternary.
            let then_branch = Box::new(self.parse_assignment()?);
            self.expect_punct(":")?;
            let else_branch = Box::new(self.parse_assignment()?);
            return Ok(Expr::Conditional {
                condition: Box::new(target),
                then_branch,
                else_branch,
            });
        }
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
        // Compound assignment `a += b` is `a = a + b`, and likewise for the
        // other arithmetic operators.
        if let Token::Punct(op) = self.peek()
            && matches!(op.as_str(), "+=" | "-=" | "*=" | "/=")
        {
            let operator = op.trim_end_matches('=').to_string();
            self.position += 1;
            let right = Box::new(self.parse_assignment()?);
            return match target {
                // A variable is a slot, not an expression with a side
                // effect — resolving its name to a slot is pure metadata, so
                // desugaring to `a = a + b` costs nothing extra to evaluate.
                Expr::Variable(name) => Ok(Expr::Assign {
                    name: name.clone(),
                    value: Box::new(Expr::Binary {
                        operator,
                        left: Box::new(Expr::Variable(name)),
                        right,
                    }),
                }),
                // A property's object and key *can* have side effects — a
                // call as the object (`getObj().n += 1`), a call as a
                // computed key (`arr[next()] += 1`) — so this compiles each
                // exactly once rather than desugaring to two references of
                // them. See `Expr::CompoundMember`.
                Expr::Member { object, key } => Ok(Expr::CompoundMember {
                    object,
                    key,
                    operator,
                    right,
                }),
                _ => Err(JsError::UnexpectedToken {
                    found: "expression".to_string(),
                    expected: "a variable or property before a compound assignment".to_string(),
                }),
            };
        }
        Ok(target)
    }

    /// The token `offset` positions ahead of the cursor.
    fn peek_at(&self, offset: usize) -> &Token {
        self.tokens
            .get(self.position + offset)
            .unwrap_or(&Token::Eof)
    }

    /// Whether an arrow function begins at the cursor: `ident =>` or a
    /// parenthesised parameter list followed by `=>`. Pure lookahead, no
    /// consumption, so an ordinary parenthesised expression is unaffected.
    fn arrow_ahead(&self) -> bool {
        if matches!(self.peek(), Token::Ident(_))
            && matches!(self.peek_at(1), Token::Punct(p) if p == "=>")
        {
            return true;
        }
        if !self.check_punct("(") {
            return false;
        }
        // Walk to the matching `)` and see whether `=>` follows it.
        let mut depth = 0;
        let mut offset = 0;
        loop {
            match self.peek_at(offset) {
                Token::Punct(p) if p == "(" => depth += 1,
                Token::Punct(p) if p == ")" => {
                    depth -= 1;
                    if depth == 0 {
                        return matches!(self.peek_at(offset + 1), Token::Punct(p) if p == "=>");
                    }
                }
                Token::Eof => return false,
                _ => {}
            }
            offset += 1;
        }
    }

    /// Parses an arrow function into the same [`Expr::Lambda`] a `function`
    /// expression produces — arrows are sugar over that machinery, so they
    /// inherit its rule that capturing an enclosing local is refused, not
    /// silently captured.
    fn parse_arrow(&mut self) -> Result<Expr, JsError> {
        let (parameters, prelude, min_arity) = if self.check_punct("(") {
            self.parse_parameter_list()?
        } else {
            // A bare, unparenthesised arrow parameter is always a plain
            // identifier in real JS too — a destructured single parameter
            // needs its own parens (`({a}) => ...`), which takes the branch
            // above. It cannot carry a default either (`x = 1 => ...` is not
            // valid JS grammar; that needs parens too), so it is always
            // required.
            let Token::Ident(name) = self.advance() else {
                return Err(JsError::UnexpectedToken {
                    found: "token".to_string(),
                    expected: "an arrow parameter".to_string(),
                });
            };
            (vec![name], Vec::new(), 1)
        };
        self.expect_punct("=>")?;
        let mut body = prelude;
        if self.check_punct("{") {
            self.position += 1;
            while !self.check_punct("}") && !matches!(self.peek(), Token::Eof) {
                body.push(self.parse_statement()?);
            }
            self.expect_punct("}")?;
        } else {
            // `x => expr` is `x => { return expr; }`.
            body.push(Stmt::Return(Some(self.parse_assignment()?)));
        }
        Ok(Expr::Lambda {
            parameters,
            body,
            min_arity,
        })
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

    /// `for (init; condition; update) body`, desugared to a block holding the
    /// init and a `while`, so no new control-flow machinery is needed. The
    /// enclosing block scopes the loop variable, and the update runs at the end
    /// of each iteration — which is what putting it after the body in the
    /// while's block achieves.
    fn parse_for(&mut self) -> Result<Stmt, JsError> {
        self.position += 1; // `for`
        self.expect_punct("(")?;
        let init = if self.eat_punct(";") {
            None
        } else {
            // A declaration or expression statement, either way consuming its
            // own `;`.
            Some(self.parse_statement()?)
        };
        let condition = if self.check_punct(";") {
            Expr::Boolean(true)
        } else {
            self.parse_expression()?
        };
        self.expect_punct(";")?;
        let update = if self.check_punct(")") {
            None
        } else {
            Some(self.parse_expression()?)
        };
        self.expect_punct(")")?;
        let body = self.parse_statement()?;

        let mut while_body = vec![body];
        if let Some(update) = update {
            while_body.push(Stmt::Expression(update));
        }
        let loop_statement = Stmt::While {
            condition,
            body: Box::new(Stmt::Block(while_body)),
        };
        let mut block = Vec::new();
        if let Some(init) = init {
            block.push(init);
        }
        block.push(loop_statement);
        Ok(Stmt::Block(block))
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
        // Prefix increment/decrement: `++x` is `x = x + 1` evaluating to the
        // new value, which is the correct prefix semantics.
        if let Token::Punct(value) = self.peek()
            && matches!(value.as_str(), "++" | "--")
        {
            let delta = if value == "++" { 1.0 } else { -1.0 };
            self.position += 1;
            let Expr::Variable(name) = self.parse_unary()? else {
                return Err(JsError::Unsupported {
                    feature: "increment/decrement of anything but a variable".to_string(),
                });
            };
            return Ok(Expr::Assign {
                name: name.clone(),
                value: Box::new(Expr::Binary {
                    operator: "+".to_string(),
                    left: Box::new(Expr::Variable(name)),
                    right: Box::new(Expr::Number(delta)),
                }),
            });
        }
        if self.check_keyword("typeof") {
            return Err(JsError::Unsupported {
                feature: "typeof".to_string(),
            });
        }
        // Real Nova usage: `delete rowEl.dataset.dragged`, `delete g[gid]` —
        // always a member expression, never a bare variable or anything
        // else `delete` can grammatically apply to (real JS allows
        // `delete x` too, though it does nothing useful outside `with`
        // blocks this engine doesn't support either). Checked ahead of
        // `parse_primary`'s blanket keyword refusal the same way `new
        // RegExp` is carved out of `new`'s.
        if self.check_keyword("delete") {
            self.position += 1;
            let operand = self.parse_unary()?;
            let Expr::Member { object, key } = operand else {
                return Err(JsError::Unsupported {
                    feature: "delete of anything but a member expression".to_string(),
                });
            };
            return Ok(Expr::Delete { object, key });
        }
        self.parse_primary()
    }

    fn parse_primary(&mut self) -> Result<Expr, JsError> {
        let primary = self.parse_primary_base()?;
        let expression = self.parse_member_suffix(primary)?;
        // Postfix increment/decrement evaluates to the *old* value, so it is
        // its own node rather than a desugaring to assignment.
        if let Token::Punct(value) = self.peek()
            && matches!(value.as_str(), "++" | "--")
        {
            let Expr::Variable(name) = expression else {
                return Err(JsError::Unsupported {
                    feature: "postfix increment/decrement of anything but a variable".to_string(),
                });
            };
            let delta = if value == "++" { 1.0 } else { -1.0 };
            self.position += 1;
            return Ok(Expr::PostUpdate { name, delta });
        }
        Ok(expression)
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
            } else if self.check_punct("(") {
                let arguments = self.parse_argument_list()?;
                object = match object {
                    // `receiver.name(args)`: a dedicated node so the
                    // receiver compiles exactly once — see
                    // `Expr::MethodCall`'s own doc comment for why this is
                    // not just `CallValue` over a `Member`.
                    Expr::Member {
                        object: receiver,
                        key,
                    } if matches!(*key, Expr::Str(_)) => {
                        let Expr::Str(name) = *key else {
                            unreachable!("checked above")
                        };
                        Expr::MethodCall {
                            object: receiver,
                            name,
                            arguments,
                        }
                    }
                    // A call applied to any other expression: an indirect
                    // call through whatever function value it produced.
                    other => Expr::CallValue {
                        callee: Box::new(other),
                        arguments,
                    },
                };
            } else {
                return Ok(object);
            }
        }
    }

    fn parse_primary_base(&mut self) -> Result<Expr, JsError> {
        // `new` is refused outright by `refuse_unsupported_keyword` below —
        // real constructors need a prototype chain this engine does not
        // model — except for the one case real usage needs: `new
        // RegExp(pattern[, flags])`, whose "instance" is just a `Value::
        // Regex` like a literal produces. Checked ahead of the blanket
        // refusal rather than added as an exception inside it, so every
        // other `new X(...)` still refuses exactly as before.
        if self.check_keyword("new") {
            return self.parse_new_expression();
        }
        self.refuse_unsupported_keyword()?;
        if self.jsx_ahead() {
            return self.parse_jsx_expression();
        }
        if self.check_punct("{") {
            return self.parse_object_literal();
        }
        if self.check_punct("[") {
            return self.parse_array_literal();
        }
        match self.advance() {
            Token::Number(text) => Ok(Expr::Number(text.parse::<f64>().unwrap_or(f64::NAN))),
            Token::Str(text) => Ok(Expr::Str(text)),
            Token::TemplateLiteral(parts) => self.desugar_template_literal(parts),
            Token::Regex(pattern, flags) => Ok(Expr::Regex { pattern, flags }),
            Token::Keyword(word) => match word.as_str() {
                "true" => Ok(Expr::Boolean(true)),
                "false" => Ok(Expr::Boolean(false)),
                "null" => Ok(Expr::Null),
                "undefined" => Ok(Expr::Undefined),
                "function" => {
                    // `function` was already consumed by `advance()`.
                    self.parse_function_expression_body()
                }
                other => Err(JsError::Unsupported {
                    feature: other.to_string(),
                }),
            },
            Token::Ident(name) => {
                if self.check_punct("(") {
                    let arguments = self.parse_argument_list()?;
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

    /// Parses a `new` expression, `new` already peeked but not consumed.
    ///
    /// Refuses everything except `new RegExp(...)` — see
    /// `parse_primary_base`'s call site for why that one case is carved
    /// out of the blanket `new` refusal.
    fn parse_new_expression(&mut self) -> Result<Expr, JsError> {
        self.position += 1; // `new`
        if !matches!(self.peek(), Token::Ident(name) if name == "RegExp") {
            return Err(JsError::Unsupported {
                feature: "constructors".to_string(),
            });
        }
        self.position += 1; // `RegExp`
        let arguments = self.parse_argument_list()?;
        if arguments.is_empty() || arguments.len() > 2 {
            return Err(JsError::Unsupported {
                feature: "`new RegExp` with anything but a pattern and an optional flags string"
                    .to_string(),
            });
        }
        Ok(Expr::NewRegExp { arguments })
    }

    /// Desugars a template literal into a chain of `+` concatenations —
    /// no dedicated AST node or opcode, since `+` here already concatenates
    /// whenever either side is a string (see `Op::Add`'s VM handling), and
    /// every template literal has at least one literal text run (possibly
    /// empty) ahead of its first interpolation, so the chain always starts
    /// from a string and every subsequent `+` stays a concatenation rather
    /// than falling through to numeric addition — the same result real
    /// template-literal semantics specify for plain (non-`toString`-
    /// overriding) values.
    ///
    /// Each interpolation's raw source text is lexed and parsed as its own
    /// standalone expression here, not inlined into this parser's own
    /// token stream — the interpolation was scanned as opaque text at the
    /// lexer level (see `scan_template_literal`) precisely because it can
    /// itself be an arbitrary expression, which only the parser knows how
    /// to read.
    fn desugar_template_literal(&mut self, parts: Vec<TemplatePart>) -> Result<Expr, JsError> {
        let mut result: Option<Expr> = None;
        for part in parts {
            let piece = match part {
                TemplatePart::Str(text) => Expr::Str(text),
                TemplatePart::Expr(source) => parse_expression_from_source(&source)?,
            };
            result = Some(match result {
                None => piece,
                Some(accumulated) => Expr::Binary {
                    operator: "+".to_string(),
                    left: Box::new(accumulated),
                    right: Box::new(piece),
                },
            });
        }
        // Unreachable in practice — `scan_template_literal` always emits at
        // least one `Str` part, even for `` ` ` `` — but a defensive
        // fallback costs nothing and keeps this total rather than panicking
        // if that invariant is ever violated.
        Ok(result.unwrap_or(Expr::Str(String::new())))
    }

    /// Parses `{ a: 1, ...rest, "b": 2, name, greet() {...} }`.
    ///
    /// Keys are identifiers, strings, or numbers, which is what the object
    /// initialiser grammar allows without computed keys — those are refused
    /// (`[expr]:` as a key changes what the initialiser means, not merely
    /// how it is written). Three real shapes follow a key: `key: value`
    /// (ordinary), `key(...) {...}` (method shorthand, desugaring to
    /// `key: function(...) {...}` — an `Expr::Lambda` value, exactly what a
    /// real `function` expression already produces), and a bare `key` with
    /// nothing after it (property shorthand for `key: key`, valid only for
    /// an identifier-origin key — `{ "a" }` or `{ 1 }` are not legal JS).
    /// Getters, setters, generator methods, and `async` methods all refuse
    /// with a typed error rather than being silently mis-parsed as some
    /// other shape — none appear in real Nova usage (confirmed by grep).
    fn parse_object_literal(&mut self) -> Result<Expr, JsError> {
        self.expect_punct("{")?;
        let mut entries = Vec::new();
        while !self.check_punct("}") {
            if self.check_punct("[") {
                return Err(JsError::Unsupported {
                    feature: "computed property keys".to_string(),
                });
            }
            if self.eat_punct("...") {
                entries.push(ObjectEntry::Spread(self.parse_assignment()?));
                if !self.eat_punct(",") {
                    break;
                }
                continue;
            }
            let key_is_ident = matches!(self.peek(), Token::Ident(_));
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
            if self.check_punct("(") {
                let (parameters, prelude, min_arity) = self.parse_parameter_list()?;
                self.expect_punct("{")?;
                let mut body = prelude;
                while !self.check_punct("}") && !matches!(self.peek(), Token::Eof) {
                    body.push(self.parse_statement()?);
                }
                self.expect_punct("}")?;
                entries.push(ObjectEntry::Property(
                    key,
                    Expr::Lambda {
                        parameters,
                        body,
                        min_arity,
                    },
                ));
            } else if self.eat_punct(":") {
                entries.push(ObjectEntry::Property(key, self.parse_assignment()?));
            } else if self.check_punct(",") || self.check_punct("}") {
                if !key_is_ident {
                    return Err(JsError::Unsupported {
                        feature: "shorthand property with a non-identifier key".to_string(),
                    });
                }
                entries.push(ObjectEntry::Property(key.clone(), Expr::Variable(key)));
            } else {
                return Err(JsError::Unsupported {
                    feature: "getter, setter, generator, or async object-literal methods"
                        .to_string(),
                });
            }
            if !self.eat_punct(",") {
                break;
            }
        }
        self.expect_punct("}")?;
        Ok(Expr::ObjectLiteral { entries })
    }

    /// `[a, b, c]`. A trailing comma is allowed; elision (`[a, , c]`) is
    /// refused rather than silently filled with `undefined`, because a hole
    /// and an explicit `undefined` differ in the specification and this
    /// implementation does not model the difference.
    fn parse_array_literal(&mut self) -> Result<Expr, JsError> {
        self.expect_punct("[")?;
        let mut elements = Vec::new();
        while !self.check_punct("]") {
            if self.check_punct(",") {
                return Err(JsError::Unsupported {
                    feature: "array elision (holes)".to_string(),
                });
            }
            if self.check_punct("...") {
                return Err(JsError::Unsupported {
                    feature: "array spread".to_string(),
                });
            }
            elements.push(self.parse_assignment()?);
            if !self.eat_punct(",") {
                break;
            }
        }
        self.expect_punct("]")?;
        Ok(Expr::ArrayLiteral { elements })
    }

    /// Parses a function expression after the `function` keyword is consumed:
    /// `(params) { body }`. A *named* function expression is refused, because
    /// the name is only visible inside for self-reference, which is capture —
    /// the feature this first-class-function step deliberately does not add.
    fn parse_function_expression_body(&mut self) -> Result<Expr, JsError> {
        // An optional name — real Nova usage: `memo(function Toggle(...)
        // {...})`, React's devtools-name idiom for giving an inline
        // component a readable name. Consumed and dropped, not bound as a
        // capturable local: confirmed by grep across every real
        // `memo(function Name(...) {...})` in the file (8 occurrences) that
        // the name is never referenced inside its own body — it is purely
        // decorative here. A body that *did* try to self-reference the name
        // would resolve through the ordinary scope chain if an enclosing
        // binding of the same name exists, or refuse as
        // `JsError::UndefinedVariable` if none does — either way a typed
        // outcome, never a silently wrong one — so no capture machinery is
        // needed to handle that case honestly.
        if matches!(self.peek(), Token::Ident(_)) {
            self.position += 1;
        }
        let (parameters, prelude, min_arity) = self.parse_parameter_list()?;
        self.expect_punct("{")?;
        let mut body = prelude;
        while !self.check_punct("}") && !matches!(self.peek(), Token::Eof) {
            body.push(self.parse_statement()?);
        }
        self.expect_punct("}")?;
        Ok(Expr::Lambda {
            parameters,
            body,
            min_arity,
        })
    }

    /// Parses `(a, b, c)` call arguments, the `(` still ahead.
    fn parse_argument_list(&mut self) -> Result<Vec<Expr>, JsError> {
        self.expect_punct("(")?;
        let mut arguments = Vec::new();
        while !self.check_punct(")") {
            arguments.push(self.parse_expression()?);
            if !self.eat_punct(",") {
                break;
            }
        }
        self.expect_punct(")")?;
        Ok(arguments)
    }

    /// Parses `(a, b, c)` parameter names, the `(` still ahead, and returns
    /// alongside them any statements a destructured parameter needs
    /// prepended to the body — `function f({ a, b }) {...}` binds a single
    /// positional parameter (a synthetic name, since it has no source name
    /// of its own) and then destructures it as the body's first statements,
    /// the same desugar a `const { a, b } = ...` declaration goes through.
    /// A plain identifier parameter is unaffected: no synthetic name, no
    /// prelude statement, identical to before this existed.
    /// Parses `(a, b, [c, d], {e}, f = 1)`.
    ///
    /// Returns the bound parameter names, the prelude statements a
    /// destructured parameter or a default value desugars to (run at the
    /// very start of the body, before anything the caller wrote), and
    /// `min_arity` — the count of leading parameters with no default value.
    ///
    /// Real Nova usage: `over = 6`, `clr = "ac"`. A default is real,
    /// observed syntax on a *plain* (non-destructured) parameter and, in
    /// both real cases, is the last parameter in the list — every call site
    /// either omits it entirely or supplies every parameter. Scoped to
    /// exactly that trailing shape: once a plain parameter has a default,
    /// any further parameter (plain-without-default or destructured, which
    /// has no top-level default of its own) refuses rather than silently
    /// picking some other arity semantics real usage never needed.
    fn parse_parameter_list(&mut self) -> Result<(Vec<String>, Vec<Stmt>, usize), JsError> {
        self.expect_punct("(")?;
        let mut parameters = Vec::new();
        let mut prelude = Vec::new();
        let mut min_arity = 0;
        let mut seen_default = false;
        while !self.check_punct(")") {
            if self.check_punct("[") || self.check_punct("{") {
                if seen_default {
                    return Err(JsError::Unsupported {
                        feature: "a destructured parameter after a default parameter".to_string(),
                    });
                }
                let temp = self.next_pattern_temp();
                let statements = if self.check_punct("[") {
                    let bindings = self.parse_array_pattern()?;
                    desugar_array_pattern(
                        bindings,
                        Expr::Variable(temp.clone()),
                        false,
                        temp.clone(),
                    )
                } else {
                    let bindings = self.parse_object_pattern()?;
                    desugar_object_pattern(
                        bindings,
                        Expr::Variable(temp.clone()),
                        false,
                        temp.clone(),
                    )
                };
                parameters.push(temp);
                // The temp's own declaration (statements[0]) reads a
                // variable of the same name that does not exist yet — it is
                // dropped here, and the parameter binding itself (already
                // in `locals` at this slot by the time the body runs) takes
                // its place, so only the per-property reads remain.
                prelude.extend(statements.into_iter().skip(1));
                min_arity += 1;
            } else {
                let Token::Ident(parameter) = self.advance() else {
                    return Err(JsError::UnexpectedToken {
                        found: "token".to_string(),
                        expected: "a parameter name".to_string(),
                    });
                };
                if self.eat_punct("=") {
                    let default = self.parse_assignment()?;
                    // `param = param === undefined ? default : param` — the
                    // same `=== undefined` semantics (not merely falsy)
                    // `apply_pattern_default` already gives destructuring
                    // defaults, so an explicit falsy argument (`over(x, 0)`)
                    // is kept, not silently replaced.
                    prelude.push(Stmt::Expression(Expr::Assign {
                        name: parameter.clone(),
                        value: Box::new(apply_pattern_default(
                            Expr::Variable(parameter.clone()),
                            Some(default),
                        )),
                    }));
                    seen_default = true;
                } else if seen_default {
                    return Err(JsError::Unsupported {
                        feature: "a required parameter after a default parameter".to_string(),
                    });
                } else {
                    min_arity += 1;
                }
                parameters.push(parameter);
            }
            if !self.eat_punct(",") {
                break;
            }
        }
        self.expect_punct(")")?;
        Ok((parameters, prelude, min_arity))
    }

    /// Parses `[pattern] = value` or `{pattern} = value`, the `const`/`let`/
    /// `var` keyword already consumed, and desugars it into the temporary-
    /// plus-per-binding sequence `Stmt::Sequence`'s own doc comment explains
    /// the scoping reason for.
    fn parse_destructuring_declaration(&mut self, constant: bool) -> Result<Vec<Stmt>, JsError> {
        let temp = self.next_pattern_temp();
        if self.check_punct("[") {
            let bindings = self.parse_array_pattern()?;
            self.expect_punct("=")?;
            let value = self.parse_assignment()?;
            Ok(desugar_array_pattern(bindings, value, constant, temp))
        } else {
            let bindings = self.parse_object_pattern()?;
            self.expect_punct("=")?;
            let value = self.parse_assignment()?;
            Ok(desugar_object_pattern(bindings, value, constant, temp))
        }
    }

    /// A fresh, source-unreachable name for the value a destructuring
    /// pattern reads its bindings from — unreachable because a real
    /// identifier can never contain `$`, so nothing a script writes can
    /// collide with or shadow it. Counted rather than reused so each
    /// occurrence gets its own binding, in line with the compiler's
    /// last-declaration-wins scope resolution rather than depending on it.
    fn next_pattern_temp(&mut self) -> String {
        let name = format!("__pattern{}$", self.pattern_count);
        self.pattern_count += 1;
        name
    }

    /// Parses `[a, , b]` after the pattern's own `[`, refusing a rest
    /// element or a nested pattern rather than mishandling one — a hole
    /// (`,` with nothing before the next `,`/`]`) is real, observed Nova
    /// syntax and becomes `None`: a skipped slot with no binding at all.
    fn parse_array_pattern(&mut self) -> Result<ArrayPatternBindings, JsError> {
        self.expect_punct("[")?;
        let mut bindings = Vec::new();
        while !self.check_punct("]") {
            if self.check_punct(",") {
                bindings.push(None);
                self.position += 1;
                continue;
            }
            if self.check_punct("...") {
                return Err(JsError::Unsupported {
                    feature: "a rest element in array destructuring".to_string(),
                });
            }
            if !matches!(self.peek(), Token::Ident(_)) {
                return Err(JsError::Unsupported {
                    feature: "a nested pattern in array destructuring".to_string(),
                });
            }
            let Token::Ident(name) = self.advance() else {
                unreachable!("checked above")
            };
            let default = if self.eat_punct("=") {
                Some(self.parse_assignment()?)
            } else {
                None
            };
            bindings.push(Some((name, default)));
            if !self.eat_punct(",") {
                break;
            }
        }
        self.expect_punct("]")?;
        Ok(bindings)
    }

    /// Parses `{a, icon: Ic, size = 12}` after the pattern's own `{`:
    /// shorthand, renamed, and defaulted properties, the three real shapes
    /// Nova's source uses. Refuses a rest property or a nested pattern
    /// rather than mishandling one — neither appears in the real source.
    fn parse_object_pattern(&mut self) -> Result<ObjectPatternBindings, JsError> {
        self.expect_punct("{")?;
        let mut bindings = Vec::new();
        while !self.check_punct("}") {
            if self.check_punct("...") {
                return Err(JsError::Unsupported {
                    feature: "a rest property in object destructuring".to_string(),
                });
            }
            let Token::Ident(key) = self.advance() else {
                return Err(JsError::UnexpectedToken {
                    found: "token".to_string(),
                    expected: "a property name in an object pattern".to_string(),
                });
            };
            let name = if self.eat_punct(":") {
                if !matches!(self.peek(), Token::Ident(_)) {
                    return Err(JsError::Unsupported {
                        feature: "a nested pattern in object destructuring".to_string(),
                    });
                }
                let Token::Ident(renamed) = self.advance() else {
                    unreachable!("checked above")
                };
                renamed
            } else {
                key.clone()
            };
            let default = if self.eat_punct("=") {
                Some(self.parse_assignment()?)
            } else {
                None
            };
            bindings.push((key, name, default));
            if !self.eat_punct(",") {
                break;
            }
        }
        self.expect_punct("}")?;
        Ok(bindings)
    }

    // -- JSX --------------------------------------------------------------
    //
    // JSX text and attribute values are not JavaScript — quoting, comment
    // syntax, and every other token rule this lexer applies simply do not
    // apply inside them — so none of what follows consults `self.tokens`.
    // It reads `self.source` directly with its own byte cursor, threaded
    // through these methods as a plain `usize` rather than `self.position`,
    // which stays exactly where it was in the token stream throughout. Once
    // a whole JSX expression has been scanned this way, `resume_at` finds
    // the token to continue ordinary parsing from. See the module-level doc
    // comment on JSX for the calling convention this desugars to and the
    // one limitation this design does not paper over.

    /// A byte of the source at an arbitrary offset, or `None` past the end.
    fn byte_at(&self, at: usize) -> Option<u8> {
        self.source.as_bytes().get(at).copied()
    }

    /// Advances past ASCII whitespace, the only kind JSX's own grammar (tag
    /// and attribute layout) needs to skip; text content is handled
    /// separately by `jsx_text` and never calls this.
    fn skip_jsx_space(&self, mut at: usize) -> usize {
        while matches!(self.byte_at(at), Some(byte) if byte.is_ascii_whitespace()) {
            at += 1;
        }
        at
    }

    /// Whether the cursor begins a JSX expression: `<` followed immediately
    /// by an identifier (an element) or by `>` (a fragment).
    ///
    /// Pure token lookahead — deciding *that* this is JSX needs only the
    /// next token, even though parsing its content drops below the token
    /// stream. `a < b` never reaches this: `parse_comparison`'s left operand
    /// already consumed `a` before its own `<` is examined, so `<` is never
    /// the first token of a *primary* expression there. This is consulted
    /// only where a bare `<` would otherwise be an unhandled primary token
    /// and today is simply a parse error — so a false positive is
    /// impossible: anything this accepts was refused before JSX existed.
    fn jsx_ahead(&self) -> bool {
        if !self.check_punct("<") {
            return false;
        }
        matches!(self.peek_at(1), Token::Ident(_))
            || matches!(self.peek_at(1), Token::Punct(punct) if punct == ">")
    }

    /// Reads a JSX name (a tag or attribute name) starting at `cursor`.
    ///
    /// `allow_hyphen` additionally permits `-` after the first character,
    /// which real JSX allows in attribute names (`data-id`, `aria-label`)
    /// but not in tag names, where a following `-` is instead refused
    /// explicitly by the caller.
    fn jsx_read_name(&self, cursor: usize, allow_hyphen: bool) -> Result<(String, usize), JsError> {
        let is_start = |byte: u8| byte.is_ascii_alphabetic() || byte == b'_' || byte == b'$';
        let is_continue = |byte: u8| {
            byte.is_ascii_alphanumeric()
                || byte == b'_'
                || byte == b'$'
                || (allow_hyphen && byte == b'-')
        };
        match self.byte_at(cursor) {
            Some(byte) if is_start(byte) => {}
            Some(byte) => {
                return Err(JsError::UnexpectedToken {
                    found: format!("`{}`", byte as char),
                    expected: "a JSX name".to_string(),
                });
            }
            None => {
                return Err(JsError::UnexpectedToken {
                    found: "end of input".to_string(),
                    expected: "a JSX name".to_string(),
                });
            }
        }
        let mut end = cursor + 1;
        while matches!(self.byte_at(end), Some(byte) if is_continue(byte)) {
            end += 1;
        }
        Ok((self.source[cursor..end].to_string(), end))
    }

    /// Parses the source between a `{` (already consumed up to `cursor`,
    /// which points just past it) and its matching `}` as an embedded
    /// JavaScript expression: an attribute value (`onClick={handler}`) or an
    /// expression child (`{value}`).
    ///
    /// The scan tracks brace depth and skips over quoted strings so a `}`
    /// or `{` inside one (`{"a}"}`) does not miscount, but otherwise does
    /// not tokenize this span — it only needs to find the matching `}`, not
    /// to understand what is between them. What is between them is parsed
    /// properly afterward, by lexing and parsing exactly that substring
    /// with the ordinary expression grammar (`parse_expression`), which is
    /// what makes `onClick={() => count = count + 1}` — an arrow function —
    /// work for free.
    fn jsx_expr_container(&mut self, cursor: usize) -> Result<(Expr, usize), JsError> {
        let bytes = self.source.as_bytes();
        let mut index = cursor;
        let mut depth = 1_i32;
        loop {
            match bytes.get(index) {
                None => {
                    return Err(JsError::UnexpectedToken {
                        found: "end of input".to_string(),
                        expected: "a closing `}` for the JSX expression".to_string(),
                    });
                }
                Some(b'{') => {
                    depth += 1;
                    index += 1;
                }
                Some(b'}') => {
                    depth -= 1;
                    if depth == 0 {
                        break;
                    }
                    index += 1;
                }
                Some(&quote) if quote == b'"' || quote == b'\'' => {
                    let value_start = index + 1;
                    let end = self.source[value_start..]
                        .find(quote as char)
                        .map(|offset| value_start + offset)
                        .ok_or_else(|| JsError::UnexpectedToken {
                            found: "end of input".to_string(),
                            expected: "a closing quote inside the JSX expression".to_string(),
                        })?;
                    index = end + 1;
                }
                Some(_) => index += 1,
            }
        }
        let inner = self.source[cursor..index].trim();
        if inner.is_empty() {
            return Err(JsError::Unsupported {
                feature: "empty JSX expression containers (`{}`)".to_string(),
            });
        }
        if inner.starts_with("...") {
            return Err(JsError::Unsupported {
                feature: "JSX spread ({...props} / {...children})".to_string(),
            });
        }
        let expr = self.parse_embedded_expression(inner)?;
        Ok((expr, index + 1))
    }

    /// Lexes and parses `source` as a single expression, entirely on its
    /// own — a fresh `Parser` over just this substring — reusing the whole
    /// precedence chain rather than re-implementing expression parsing for
    /// JSX's embedded `{expr}` positions.
    ///
    /// Depth starts from the enclosing parser's current depth rather than
    /// zero, so deeply nested JSX with deeply nested `{expr}` inside it
    /// still refuses past `MAX_NESTING_DEPTH` overall instead of resetting
    /// the budget at each boundary.
    fn parse_embedded_expression(&mut self, source: &str) -> Result<Expr, JsError> {
        // Strict, not tolerant: this substring's tokens are the real
        // program, not a discarded eager-pass placeholder — see `lex`'s
        // own doc comment on `tolerate_unknown`.
        let (tokens, starts) = lex(source, false)?;
        let mut embedded = Parser::new(source, tokens, starts);
        embedded.depth = self.depth;
        let expr = embedded.parse_expression()?;
        if !matches!(embedded.peek(), Token::Eof) {
            return Err(JsError::UnexpectedToken {
                found: embedded.peek().describe(),
                expected: "end of the JSX expression".to_string(),
            });
        }
        Ok(expr)
    }

    /// Scans a run of JSX text starting at `cursor`, stopping before `<` or
    /// `{` (or the end of input). Returns the child expression to emit, if
    /// any, and the offset of the character it stopped at.
    ///
    /// A run that is nothing but whitespace contributes no child at all —
    /// otherwise every line break and indent in ordinarily-formatted
    /// multi-line JSX (exactly what a 1500-tag hand-formatted source file
    /// contains) would show up as a spurious whitespace-only string
    /// argument to `createElement`. A run with any non-whitespace content
    /// is kept verbatim, spacing included: this implementation does not
    /// attempt JSX's fuller per-line trim-and-rejoin whitespace algorithm,
    /// only the one rule needed to keep formatting-only whitespace out of
    /// the desugared call.
    fn jsx_text(&self, cursor: usize) -> (Option<Expr>, usize) {
        let bytes = self.source.as_bytes();
        let mut index = cursor;
        while !matches!(bytes.get(index), None | Some(b'<') | Some(b'{')) {
            index += 1;
        }
        let raw = &self.source[cursor..index];
        if raw.trim().is_empty() {
            (None, index)
        } else {
            (Some(Expr::Str(raw.to_string())), index)
        }
    }

    /// Parses JSX children starting at `cursor` up to and including the
    /// matching closing tag, returning the children in source order and the
    /// offset just past that closing tag's `>`.
    ///
    /// `name` is `None` for a fragment, matched against a bare `</>`, or
    /// `Some(tag)` for an element, matched against `</tag>`. A closing tag
    /// that does not match — or none before the input ends — is a parse
    /// error naming what was expected, never a silent pairing with whatever
    /// closes next.
    fn jsx_children(
        &mut self,
        mut cursor: usize,
        name: Option<&str>,
    ) -> Result<(Vec<Expr>, usize), JsError> {
        let mut children = Vec::new();
        loop {
            match self.byte_at(cursor) {
                None => {
                    return Err(JsError::UnexpectedToken {
                        found: "end of input".to_string(),
                        expected: format!("a closing tag `</{}>`", name.unwrap_or_default()),
                    });
                }
                Some(b'{') => {
                    let (expr, next) = self.jsx_expr_container(cursor + 1)?;
                    children.push(expr);
                    cursor = next;
                }
                Some(b'<') if self.byte_at(cursor + 1) == Some(b'/') => {
                    let mut after = cursor + 2;
                    let closing_name = if self.byte_at(after) == Some(b'>') {
                        None
                    } else {
                        let (name, next) = self.jsx_read_name(after, true)?;
                        after = next;
                        Some(name)
                    };
                    after = self.skip_jsx_space(after);
                    if self.byte_at(after) != Some(b'>') {
                        return Err(JsError::UnexpectedToken {
                            found: "token".to_string(),
                            expected: "`>` to close the JSX closing tag".to_string(),
                        });
                    }
                    if closing_name.as_deref() != name {
                        return Err(JsError::UnexpectedToken {
                            found: format!("closing tag `</{}>`", closing_name.unwrap_or_default()),
                            expected: format!(
                                "the matching closing tag `</{}>`",
                                name.unwrap_or_default()
                            ),
                        });
                    }
                    return Ok((children, after + 1));
                }
                Some(b'<') => {
                    let (expr, next) = self.jsx_element(cursor)?;
                    children.push(expr);
                    cursor = next;
                }
                Some(_) => {
                    let (text, next) = self.jsx_text(cursor);
                    if let Some(text) = text {
                        children.push(text);
                    }
                    cursor = next;
                }
            }
        }
    }

    /// Parses `name="value"` and `name={expr}` attributes starting at
    /// `cursor`, stopping (without consuming) at the `/` or `>` that ends
    /// the opening tag.
    fn jsx_attributes(
        &mut self,
        mut cursor: usize,
    ) -> Result<(Vec<(String, Expr)>, usize), JsError> {
        let mut entries = Vec::new();
        loop {
            cursor = self.skip_jsx_space(cursor);
            match self.byte_at(cursor) {
                Some(b'/' | b'>') | None => break,
                _ => {}
            }
            if self.source[cursor..].starts_with("{...") {
                return Err(JsError::Unsupported {
                    feature: "JSX spread attributes ({...props})".to_string(),
                });
            }
            let (name, mut after_name) = self.jsx_read_name(cursor, true)?;
            if self.byte_at(after_name) == Some(b'.') {
                return Err(JsError::Unsupported {
                    feature: "namespaced JSX attribute names".to_string(),
                });
            }
            after_name = self.skip_jsx_space(after_name);
            if self.byte_at(after_name) != Some(b'=') {
                return Err(JsError::Unsupported {
                    feature: "boolean-shorthand JSX attributes (write e.g. `x={true}` explicitly)"
                        .to_string(),
                });
            }
            let value_cursor = self.skip_jsx_space(after_name + 1);
            let (value, next) = match self.byte_at(value_cursor) {
                Some(quote) if quote == b'"' || quote == b'\'' => {
                    let value_start = value_cursor + 1;
                    let end = self.source[value_start..]
                        .find(quote as char)
                        .map(|offset| value_start + offset)
                        .ok_or_else(|| JsError::UnexpectedToken {
                            found: "end of input".to_string(),
                            expected: format!(
                                "a closing `{}` for the attribute value",
                                quote as char
                            ),
                        })?;
                    (
                        Expr::Str(self.source[value_start..end].to_string()),
                        end + 1,
                    )
                }
                Some(b'{') => self.jsx_expr_container(value_cursor + 1)?,
                _ => {
                    return Err(JsError::UnexpectedToken {
                        found: "token".to_string(),
                        expected: "a quoted string or `{expression}` after `=`".to_string(),
                    });
                }
            };
            entries.push((name, value));
            cursor = next;
        }
        Ok((entries, cursor))
    }

    /// Parses one JSX element or fragment starting at the `<` at `cursor`
    /// and desugars it into a `createElement` call (see the module-level
    /// doc comment on JSX for the exact convention), returning that
    /// expression and the offset just past its own closing — or
    /// self-closing — tag.
    ///
    /// Wrapped by [`Self::enter`]/[`Self::leave`] like every other
    /// recursive grammar production in this parser, so `<a><a><a>…` refuses
    /// past [`MAX_NESTING_DEPTH`] rather than overflowing the stack — this
    /// recursion is on the native call stack the same as any other, even
    /// though it walks raw source instead of tokens.
    fn jsx_element(&mut self, cursor: usize) -> Result<(Expr, usize), JsError> {
        self.enter()?;
        let result = self.jsx_element_inner(cursor);
        self.leave();
        result
    }

    fn jsx_element_inner(&mut self, cursor: usize) -> Result<(Expr, usize), JsError> {
        // `cursor` is the `<`; `jsx_ahead` already confirmed an identifier
        // or `>` follows.
        let after_angle = cursor + 1;
        if self.byte_at(after_angle) == Some(b'>') {
            // A fragment, `<>...</>`, desugars to a call naming `Fragment`
            // as a variable reference rather than a string — the same
            // convention a component reference uses, and consistent with
            // it being a real (if special) value in scope rather than a
            // host/intrinsic tag name. It carries no attributes.
            let (children, end) = self.jsx_children(after_angle + 1, None)?;
            return Ok((
                Expr::Call {
                    callee: "__jsxCreateElement".to_string(),
                    arguments: vec![
                        Expr::Variable("Fragment".to_string()),
                        Expr::ObjectLiteral {
                            entries: Vec::new(),
                        },
                        Expr::ArrayLiteral { elements: children },
                    ],
                },
                end,
            ));
        }

        let (tag_name, after_name) = self.jsx_read_name(after_angle, false)?;
        if matches!(self.byte_at(after_name), Some(b'.' | b'-')) {
            return Err(JsError::Unsupported {
                feature: "namespaced or hyphenated JSX tag names (e.g. `<Foo.Bar>`)".to_string(),
            });
        }
        let (attributes, after_attrs) = self.jsx_attributes(after_name)?;
        // Lowercase-leading names are host/intrinsic elements and pass as a
        // string; uppercase-leading names are component references and
        // pass as the identifier itself, evaluated like any other variable
        // — matching real JSX semantics exactly, and meaning an
        // undeclared component name fails to compile as `UndefinedVariable`
        // rather than silently stringifying it.
        let tag_arg = if tag_name.starts_with(|c: char| c.is_ascii_uppercase()) {
            Expr::Variable(tag_name.clone())
        } else {
            Expr::Str(tag_name.clone())
        };
        let props_arg = Expr::ObjectLiteral {
            entries: attributes
                .into_iter()
                .map(|(key, value)| ObjectEntry::Property(key, value))
                .collect(),
        };

        if self.byte_at(after_attrs) == Some(b'/') {
            if self.byte_at(after_attrs + 1) != Some(b'>') {
                return Err(JsError::UnexpectedToken {
                    found: "token".to_string(),
                    expected: "`/>` to self-close the JSX tag".to_string(),
                });
            }
            return Ok((
                Expr::Call {
                    callee: "__jsxCreateElement".to_string(),
                    arguments: vec![
                        tag_arg,
                        props_arg,
                        Expr::ArrayLiteral {
                            elements: Vec::new(),
                        },
                    ],
                },
                after_attrs + 2,
            ));
        }
        if self.byte_at(after_attrs) != Some(b'>') {
            return Err(JsError::UnexpectedToken {
                found: "token".to_string(),
                expected: "`>` or `/>` to close the JSX opening tag".to_string(),
            });
        }
        let (children, end) = self.jsx_children(after_attrs + 1, Some(&tag_name))?;
        Ok((
            Expr::Call {
                callee: "__jsxCreateElement".to_string(),
                arguments: vec![
                    tag_arg,
                    props_arg,
                    Expr::ArrayLiteral { elements: children },
                ],
            },
            end,
        ))
    }

    /// Entry point called from `parse_primary_base` once `jsx_ahead`
    /// confirms a JSX expression starts here. Scans it from the raw source
    /// and then hands control back to ordinary token-based parsing.
    fn parse_jsx_expression(&mut self) -> Result<Expr, JsError> {
        let start = self.starts[self.position];
        let (expr, end) = self.jsx_element(start)?;
        self.resume_at(end)?;
        Ok(expr)
    }

    /// After a raw-source JSX scan ending at byte offset `byte_offset`,
    /// resumes ordinary token-based parsing at the first token starting at
    /// or after it.
    ///
    /// Every delimiter this scanner stops on (`<`, `>`, `/`, `{`, `}`, and
    /// quotes) is also individually tokenized by the plain lexer no matter
    /// what precedes it, so as long as JSX text and attribute content stay
    /// within the plain lexer's own supported character set, `byte_offset`
    /// lands at the next pre-lexed token's start — modulo ordinary
    /// insignificant whitespace between the two, which this skips over
    /// exactly as the plain lexer itself does everywhere else in the file
    /// (`<div>hi</div>\n)` is not meaningfully different from
    /// `<div>hi</div>)`, and treating trailing whitespace after a JSX
    /// expression as a desync would refuse ordinarily-formatted, multi-line
    /// JSX wrapped in parentheses — a real gap this exact case caught,
    /// since no earlier test happened to leave whitespace there. What is
    /// still checked, and still refused, is any *non-whitespace* gap: JSX
    /// content that desynchronises the eager whole-file lex (most plausibly
    /// an unescaped quote inside text, since this lexer has no escape
    /// sequences) leaves a real, consumed token behind that this alignment
    /// check would otherwise silently skip past. Fixing that case outright
    /// would need the tokenizer to be JSX-context-aware — lexing on demand
    /// as the parser asks for tokens, rather than the whole file eagerly up
    /// front — which is a larger change than this syntax-layer step makes;
    /// this is the honest boundary of what it does instead.
    fn resume_at(&mut self, byte_offset: usize) -> Result<(), JsError> {
        self.position = self.starts.partition_point(|&start| start < byte_offset);
        let after_whitespace = self.skip_jsx_space(byte_offset);
        let aligned = match self.starts.get(self.position) {
            Some(&start) => start == after_whitespace,
            // No further token: alignment only holds if nothing but
            // whitespace remains before the true end of the source.
            None => after_whitespace == self.source.len(),
        };
        if !aligned {
            return Err(JsError::Unsupported {
                feature: "a JSX text or attribute value using a character (most likely a quote) \
                          that the plain lexer would read differently, desynchronising the \
                          tokens that follow the JSX expression"
                    .to_string(),
            });
        }
        Ok(())
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
/// The array index a property key denotes, if it is a canonical non-negative
/// integer index. `"0"`, `"42"` are indices; `"length"`, `"01"`, `"-1"` are
/// ordinary keys and return `None`. Canonical form only, so `"01"` parses but
/// is not index 1.
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
            // Both object and array values are heap references this data
            // keeps alive; missing either collects a live value.
            match value {
                Value::Object(reference) | Value::Array(reference) | Value::Closure(reference) => {
                    out.push(*reference);
                }
                _ => {}
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

    /// Removes a property if present, for `delete`. `O(n)` in the object's
    /// own size — every entry after the removed one shifts down by one
    /// position in `entries`, and `index` must track that shift so a later
    /// lookup does not read the wrong slot — accepted the same way this
    /// object model accepts other small-object-sized costs elsewhere (real
    /// usage deletes from short-lived UI-state maps, not documents).
    fn remove(&mut self, key: &str) {
        let Some(at) = self.index.remove(key) else {
            return;
        };
        self.entries.remove(at);
        for position in self.index.values_mut() {
            if *position > at {
                *position -= 1;
            }
        }
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
    /// Push the value of global slot `n` — a top-level `const`/`let`/`var`
    /// binding, reachable from a function body at any nesting depth. Unlike
    /// [`Op::LoadUpvalue`] this is not a capture: the storage is the shared
    /// global table, not a snapshot taken when a closure was created, so it
    /// always reads whatever the binding currently holds.
    LoadGlobal(usize),
    /// Store the top of stack into global slot `n`, leaving it on the stack.
    StoreGlobal(usize),
    /// Allocate an empty object and push a handle to it.
    NewObject,
    /// Pop `n` elements and push an array of them, element 0 deepest.
    NewArray(usize),
    /// Push a copy of the top of stack.
    Dup,
    /// Push a copy of the top two stack values, in the same order: `[.., a,
    /// b]` becomes `[.., a, b, a, b]`. Used by compound property assignment
    /// to read an object/key pair's current value and then write the new one
    /// through the same pair, without recompiling — and so
    /// re-evaluating — the object and key expressions a second time.
    Dup2,
    /// Call a bound operation by name with `n` arguments from the stack.
    HostCall(String, usize),
    /// Indirect call: pop `argc` arguments then the callee (a function value)
    /// and run it, pushing the result.
    CallValue {
        argc: usize,
    },
    /// Pop `argc` arguments then the receiver; call `name` as a method on
    /// it. An own property of the receiver named `name` holding a function
    /// or closure runs first if present; otherwise a built-in String/Array
    /// method with that name runs directly against the receiver, refusing
    /// with a typed error if neither applies.
    CallMethod {
        name: String,
        argc: usize,
    },
    /// Pop `upvalues` captured values and push a closure over function
    /// `index`. The values were pushed in upvalue order, index 0 deepest.
    MakeClosure {
        index: usize,
        upvalues: usize,
    },
    /// Push the current frame's captured upvalue at `0`-based index.
    LoadUpvalue(usize),
    /// Pop a function or closure value and queue it as a microtask, pushing
    /// `undefined` (`queueMicrotask`'s own return value).
    QueueMicrotask,
    /// Pop key then object; push the property value, or `undefined`.
    GetProperty,
    /// Pop value, key, object; set the property and push the value back.
    SetProperty,
    /// Pop key then object; remove the property if present and push
    /// `true` — real JS `delete` semantics for a configurable own property
    /// (which is every property this engine's object model has, since it
    /// does not model non-configurable ones), true regardless of whether
    /// the key existed to begin with.
    DeleteProperty,
    /// Pop source, then target; copy every own property of `source` onto
    /// `target` (spreading nothing for `null`/`undefined`) and push
    /// `target` back. Used by object-literal spread (`{...source}`).
    SpreadInto,
    /// Pop `argc` arguments (a pattern string, then an optional flags
    /// string) and push the `Value::Regex` `new RegExp(...)` compiles them
    /// into. Unlike a regex literal's `Op::Const`, this compiles the
    /// pattern at run time, since the pattern is an arbitrary runtime
    /// string here rather than fixed source text.
    ConstructRegex {
        argc: usize,
    },
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
    /// Parameter count — the most arguments a call may pass.
    pub arity: usize,
    /// The fewest arguments a call may pass — the count of leading
    /// parameters with no default value. Equal to `arity` for a function
    /// with no default parameters. A call site is valid when `min_arity <=
    /// argc <= arity`; the VM's own frame setup already fills any local
    /// slot beyond `argc` with `Value::Undefined` regardless of this field
    /// (see `run_function_with_upvalues`), so no other runtime change is
    /// needed to support default parameters — each defaulted parameter's
    /// own body prelude (`param = param === undefined ? default : param`,
    /// built by `apply_pattern_default`) is what actually applies the
    /// default when a caller omitted it.
    pub min_arity: usize,
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

#[derive(Clone)]
struct Scope {
    names: Vec<(String, bool)>,
    /// Slot index where this scope's names begin.
    base: usize,
}

/// One captured variable of the function currently being compiled: the name,
/// and the slot it occupies in the immediately enclosing function's frame.
struct Upvalue {
    name: String,
    parent_slot: usize,
}

struct Compiler {
    functions: Vec<Function>,
    /// Function name to table index, resolved for calls: `(name, index,
    /// min_arity, arity)` — see [`Function::min_arity`]'s doc comment.
    signatures: Vec<(String, usize, usize, usize)>,
    /// Top-level `const`/`let`/`var` bindings, name to global slot plus
    /// whether reassignment is refused. Unlike `scopes`, this is never saved
    /// or swapped by `fill_function` — a script-level binding is visible to a
    /// function body at any nesting depth, not just the direct parent that
    /// `resolve_upvalue`'s single-level capture allows.
    globals: Vec<(String, bool)>,
    scopes: Vec<Scope>,
    code: Vec<Op>,
    next_slot: usize,
    max_slot: usize,
    /// The immediately enclosing function's scopes, present while a nested
    /// function body is being compiled, so a free variable can be resolved as
    /// a capture from the parent. Single level: only the direct parent is
    /// visible, and a reference reaching further is refused.
    enclosing_scopes: Option<Vec<Scope>>,
    /// The upvalues the function currently being compiled captures, in the
    /// order it will read them.
    upvalues: Vec<Upvalue>,
}

impl Compiler {
    fn new() -> Self {
        Self {
            functions: Vec::new(),
            signatures: Vec::new(),
            globals: Vec::new(),
            scopes: Vec::new(),
            code: Vec::new(),
            next_slot: 0,
            max_slot: 0,
            enclosing_scopes: None,
            upvalues: Vec::new(),
        }
    }

    fn compile(mut self, statements: &[Stmt]) -> Result<Program, JsError> {
        // Functions are hoisted so a call can appear before the declaration,
        // and so mutual recursion resolves.
        for statement in statements {
            if let Stmt::Function {
                name,
                parameters,
                min_arity,
                ..
            } = statement
            {
                let index = self.signatures.len() + 1;
                self.signatures
                    .push((name.clone(), index, *min_arity, parameters.len()));
            }
        }
        // Top-level `const`/`let`/`var` bindings are hoisted into the flat
        // global table before any body is compiled, so a function declared
        // earlier in source order can still reference one declared later —
        // the same hoisting `signatures` already gets, for the same reason.
        // A name already seen keeps its first slot: `var`'s redeclaration is
        // not a compile error here.
        //
        // Recurses into `Stmt::Sequence` (a destructuring declaration or an
        // import statement's desugar, both of which produce their bindings
        // this way): a top-level `const [a, b] = x;` or `import { X as Y }
        // from "...";` runs in the *current* scope — the global scope, at
        // this level — exactly like a bare `Stmt::Declare` would, and must
        // hoist the same way or a forward reference to it resolves through
        // no fallback at all (fails as an unbound host operation, not as
        // the clearer "not defined yet" an ordinary missing declaration
        // gives).
        fn hoist_declares(statements: &[Stmt], globals: &mut Vec<(String, bool)>) {
            for statement in statements {
                match statement {
                    Stmt::Declare { name, constant, .. } => {
                        if !globals.iter().any(|(existing, _)| existing == name) {
                            globals.push((name.clone(), *constant));
                        }
                    }
                    Stmt::Sequence(inner) => hoist_declares(inner, globals),
                    _ => {}
                }
            }
        }
        hoist_declares(statements, &mut self.globals);
        // Reserve slot 0 for the top level and one slot per declared function,
        // so a nested function *expression* pushed while compiling a body
        // lands after them rather than displacing a declared index.
        let placeholder = || Function {
            name: "<reserved>".to_string(),
            arity: 0,
            min_arity: 0,
            locals: 0,
            code: Vec::new(),
        };
        self.functions.push(placeholder());
        let declared = statements
            .iter()
            .filter(|s| matches!(s, Stmt::Function { .. }))
            .count();
        for _ in 0..declared {
            self.functions.push(placeholder());
        }
        let mut index = 1;
        for statement in statements {
            if let Stmt::Function {
                name,
                parameters,
                body,
                min_arity,
            } = statement
            {
                // A top-level declaration has no enclosing function to
                // capture from; any upvalues would be a compiler bug.
                let captured =
                    self.fill_function(index, name, parameters, body, *min_arity, None)?;
                debug_assert!(captured.is_empty());
                index += 1;
            }
        }

        self.push_scope();
        for statement in statements {
            self.compile_top_level_statement(statement)?;
        }
        self.pop_scope();
        self.code.push(Op::Const(Value::Undefined));
        self.code.push(Op::Return);

        let locals = self.max_slot;
        let code = core::mem::take(&mut self.code);
        self.functions[0] = Function {
            name: "<top>".to_string(),
            arity: 0,
            min_arity: 0,
            locals,
            code,
        };
        Ok(Program {
            functions: self.functions,
        })
    }

    /// Compiles one program-top-level statement, the way the top-level
    /// script body needs — not the way a statement nested inside a
    /// function body would (see `Self::statement` for that).
    ///
    /// A direct `Stmt::Declare` here stores into its hoisted global slot
    /// rather than a local scope slot, so it stays visible from a function
    /// body at any depth. `Stmt::Sequence` (a destructuring declaration or
    /// an import statement's desugar, both of which produce their bindings
    /// this way) recurses through this same method for each inner
    /// statement — it runs in the *current* scope, which at this level
    /// *is* top-level, so its own `Stmt::Declare`s need the identical
    /// global-slot treatment, not the generic per-scope-local compiling
    /// `Self::statement` would give them (that mismatch was a real,
    /// previously-latent bug: the slot was reserved by hoisting but never
    /// written, so a global reached this way silently read back
    /// `undefined` — caught because an import-created alias binding was
    /// the first top-level use of `Stmt::Sequence` this engine had ever
    /// compiled; a nested-inside-a-function-body destructuring statement
    /// takes the ordinary local-scope path from `Self::statement` and was
    /// never affected).
    fn compile_top_level_statement(&mut self, statement: &Stmt) -> Result<(), JsError> {
        match statement {
            Stmt::Function { .. } => Ok(()),
            Stmt::Declare { name, value, .. } => {
                match value {
                    Some(expression) => self.expression(expression)?,
                    None => self.code.push(Op::Const(Value::Undefined)),
                }
                let slot = self
                    .globals
                    .iter()
                    .position(|(existing, _)| existing == name)
                    .expect("every top-level declare was hoisted above");
                self.code.push(Op::StoreGlobal(slot));
                self.code.push(Op::Pop);
                Ok(())
            }
            Stmt::Sequence(inner) => {
                for statement in inner {
                    self.compile_top_level_statement(statement)?;
                }
                Ok(())
            }
            other => self.statement(other),
        }
    }

    /// Compiles a function body into the already-reserved slot `index`.
    ///
    /// `enclosing` is the scope set of the directly-enclosing function, present
    /// for a nested lambda and absent for a top-level declaration. A free
    /// variable resolving to a `const` in `enclosing` is captured as an
    /// upvalue; a `let`/`var` there is refused (capture of a mutable binding
    /// would need by-reference cells this step does not build); a name reaching
    /// further than one level, or nowhere, is refused as undefined. Returns the
    /// upvalues captured, in the order the body reads them.
    fn fill_function(
        &mut self,
        index: usize,
        name: &str,
        parameters: &[String],
        body: &[Stmt],
        min_arity: usize,
        enclosing: Option<Vec<Scope>>,
    ) -> Result<Vec<Upvalue>, JsError> {
        let outer_code = core::mem::take(&mut self.code);
        let outer_scopes = core::mem::take(&mut self.scopes);
        let outer_enclosing = core::mem::replace(&mut self.enclosing_scopes, enclosing);
        let outer_upvalues = core::mem::take(&mut self.upvalues);
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

        self.functions[index] = Function {
            name: name.to_string(),
            arity: parameters.len(),
            min_arity,
            locals: self.max_slot,
            code: core::mem::take(&mut self.code),
        };

        let captured = core::mem::replace(&mut self.upvalues, outer_upvalues);
        self.enclosing_scopes = outer_enclosing;
        self.code = outer_code;
        self.scopes = outer_scopes;
        self.next_slot = outer_next;
        self.max_slot = outer_max;
        Ok(captured)
    }

    /// Reserves a slot, compiles a lambda body capturing from the current
    /// (enclosing) scopes, and returns its index and captured upvalues.
    fn compile_lambda(
        &mut self,
        parameters: &[String],
        body: &[Stmt],
        min_arity: usize,
    ) -> Result<(usize, Vec<Upvalue>), JsError> {
        let index = self.functions.len();
        self.functions.push(Function {
            name: "<anonymous>".to_string(),
            arity: 0,
            min_arity: 0,
            locals: 0,
            code: Vec::new(),
        });
        // The lambda captures from wherever it is defined: the current scopes.
        let enclosing = self.scopes.clone();
        let captured = self.fill_function(
            index,
            "<anonymous>",
            parameters,
            body,
            min_arity,
            Some(enclosing),
        )?;
        Ok((index, captured))
    }

    /// Resolves a free variable as a capture from the enclosing function.
    ///
    /// Returns the upvalue index if the name is a `const` in the enclosing
    /// scopes (registering it on first use). A mutable enclosing binding is
    /// refused. A name not in the single enclosing level returns `None`, so the
    /// caller falls through to the undefined refusal.
    fn resolve_upvalue(&mut self, name: &str) -> Result<Option<usize>, JsError> {
        if let Some(existing) = self.upvalues.iter().position(|u| u.name == name) {
            return Ok(Some(existing));
        }
        let Some(enclosing) = &self.enclosing_scopes else {
            return Ok(None);
        };
        let mut found = None;
        for scope in enclosing {
            for (offset, (candidate, constant)) in scope.names.iter().enumerate() {
                if candidate == name {
                    found = Some((scope.base + offset, *constant));
                }
            }
        }
        match found {
            Some((slot, true)) => {
                self.upvalues.push(Upvalue {
                    name: name.to_string(),
                    parent_slot: slot,
                });
                Ok(Some(self.upvalues.len() - 1))
            }
            Some((_, false)) => Err(JsError::Unsupported {
                feature: format!(
                    "capturing the mutable binding `{name}`; capture a const, \
                     or by-reference capture is not yet implemented"
                ),
            }),
            None => Ok(None),
        }
    }

    /// Resolves a name against the top-level global table: slot and whether
    /// reassignment is refused. Unlike `resolve`/`resolve_upvalue`, this
    /// check does not depend on nesting depth or which function is currently
    /// being compiled — `globals` is never swapped by `fill_function`.
    fn global_slot(&self, name: &str) -> Option<(usize, bool)> {
        self.globals
            .iter()
            .position(|(candidate, _)| candidate == name)
            .map(|slot| (slot, self.globals[slot].1))
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
            Stmt::Sequence(statements) => {
                // No push_scope/pop_scope: these bindings belong to whatever
                // scope this Sequence itself sits in — a destructuring
                // declaration is one statement in the source, and every name
                // it introduces must outlive this call the same way a plain
                // `const` would.
                for inner in statements {
                    self.statement(inner)?;
                }
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
            // Compiled to a matcher exactly once, here — every execution of
            // this literal (in a loop, in a repeatedly-called function)
            // just clones the `Rc`, not the pattern. See `Value::Regex`'s
            // own doc comment.
            Expr::Regex { pattern, flags } => {
                let compiled = regex::compile_pattern(pattern, flags).map_err(|error| {
                    JsError::Unsupported {
                        feature: format!("the regular expression /{pattern}/{flags}: {error}"),
                    }
                })?;
                self.code.push(Op::Const(Value::Regex(Rc::new(compiled))));
            }
            Expr::NewRegExp { arguments } => {
                for argument in arguments {
                    self.expression(argument)?;
                }
                self.code.push(Op::ConstructRegex {
                    argc: arguments.len(),
                });
            }
            Expr::Variable(name) => {
                if let Some((slot, _)) = self.resolve(name) {
                    self.code.push(Op::LoadLocal(slot));
                } else if let Some(upvalue) = self.resolve_upvalue(name)? {
                    self.code.push(Op::LoadUpvalue(upvalue));
                } else if let Some(&(_, index, ..)) = self
                    .signatures
                    .iter()
                    .find(|(candidate, ..)| candidate == name)
                {
                    // A top-level `function` declaration referenced as a
                    // plain value (stored, passed as a callback, used as a
                    // JSX tag) rather than called directly. Its identity is
                    // fixed at compile time, so this is a constant, not a
                    // global slot read.
                    self.code.push(Op::Const(Value::Function(index)));
                } else if let Some((slot, _)) = self.global_slot(name) {
                    self.code.push(Op::LoadGlobal(slot));
                } else {
                    return Err(JsError::UndefinedVariable { name: name.clone() });
                }
            }
            Expr::Assign { name, value } => {
                if let Some((slot, constant)) = self.resolve(name) {
                    if constant {
                        return Err(JsError::AssignmentToConstant { name: name.clone() });
                    }
                    self.expression(value)?;
                    self.code.push(Op::StoreLocal(slot));
                } else if let Some((slot, constant)) = self.global_slot(name) {
                    if constant {
                        return Err(JsError::AssignmentToConstant { name: name.clone() });
                    }
                    self.expression(value)?;
                    self.code.push(Op::StoreGlobal(slot));
                } else {
                    return Err(JsError::UndefinedVariable { name: name.clone() });
                }
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
            Expr::Conditional {
                condition,
                then_branch,
                else_branch,
            } => {
                // Only the taken branch runs: `emit_jump_if_false` consumes
                // the condition (unlike `Expr::Logical`'s peek variants,
                // whose own operand is also the result), so both branches
                // push exactly one value and the two paths rejoin balanced.
                self.expression(condition)?;
                let to_else = self.emit_jump_if_false();
                self.expression(then_branch)?;
                let to_end = self.emit_jump();
                self.patch(to_else);
                self.expression(else_branch)?;
                self.patch(to_end);
            }
            Expr::MethodCall {
                object,
                name,
                arguments,
            } => {
                self.expression(object)?;
                for argument in arguments {
                    self.expression(argument)?;
                }
                self.code.push(Op::CallMethod {
                    name: name.clone(),
                    argc: arguments.len(),
                });
            }
            Expr::ObjectLiteral { entries } => {
                self.code.push(Op::NewObject);
                for entry in entries {
                    // Both SetProperty and SpreadInto consume the object, so
                    // each entry works on a copy and the original stays for
                    // the next one. Without the duplicate the first entry
                    // empties the stack and every later access reads a
                    // property of `undefined`.
                    self.code.push(Op::Dup);
                    match entry {
                        ObjectEntry::Property(key, value) => {
                            self.code.push(Op::Const(Value::String(key.clone())));
                            self.expression(value)?;
                            self.code.push(Op::SetProperty);
                        }
                        ObjectEntry::Spread(source) => {
                            self.expression(source)?;
                            self.code.push(Op::SpreadInto);
                        }
                    }
                    // Both ops leave a value (SetProperty the assigned value,
                    // SpreadInto the object itself); drop it so only the
                    // original object remains.
                    self.code.push(Op::Pop);
                }
            }
            Expr::ArrayLiteral { elements } => {
                // Elements are pushed in source order, element 0 deepest, and
                // NewArray gathers them; keeping the count on the op means the
                // VM does not scan for a marker.
                for element in elements {
                    self.expression(element)?;
                }
                self.code.push(Op::NewArray(elements.len()));
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
            Expr::Delete { object, key } => {
                self.expression(object)?;
                self.expression(key)?;
                self.code.push(Op::DeleteProperty);
            }
            Expr::Call { callee, arguments } => {
                // Resolution order: a declared function wins a name collision
                // (a program's own declaration is not shadowed by the host);
                // then a local variable holding a function value (an indirect
                // call); then a host-bound operation, checked at the call
                // because the compiler does not hold the host's table.
                if let Some(&(_, index, min_arity, arity)) =
                    self.signatures.iter().find(|(name, ..)| name == callee)
                {
                    if arguments.len() < min_arity || arguments.len() > arity {
                        return Err(JsError::TypeError {
                            message: format!(
                                "{callee} expects {} argument(s), got {}",
                                arity_range(min_arity, arity),
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
                } else if let Some((slot, _)) = self.resolve(callee) {
                    // A local holds a function value: load it, then the args,
                    // then call indirectly.
                    self.code.push(Op::LoadLocal(slot));
                    for argument in arguments {
                        self.expression(argument)?;
                    }
                    self.code.push(Op::CallValue {
                        argc: arguments.len(),
                    });
                } else if let Some(upvalue) = self.resolve_upvalue(callee)? {
                    // A captured function value.
                    self.code.push(Op::LoadUpvalue(upvalue));
                    for argument in arguments {
                        self.expression(argument)?;
                    }
                    self.code.push(Op::CallValue {
                        argc: arguments.len(),
                    });
                } else if let Some((slot, _)) = self.global_slot(callee) {
                    // A top-level `const`/`let` holding a function value
                    // (an arrow function or function expression, as opposed
                    // to a `function` declaration, which took the fast path
                    // above), called from any nesting depth.
                    self.code.push(Op::LoadGlobal(slot));
                    for argument in arguments {
                        self.expression(argument)?;
                    }
                    self.code.push(Op::CallValue {
                        argc: arguments.len(),
                    });
                } else if callee == "queueMicrotask" {
                    // A VM-native builtin, not a host operation: it must
                    // reach the interpreter's own microtask queue, which a
                    // `Host` implementation has no access to. Checked last,
                    // like a host op, so a script's own declaration of the
                    // same name still wins — consistent with every other
                    // name in this resolution order.
                    if arguments.len() != 1 {
                        return Err(JsError::OperationArity {
                            name: callee.clone(),
                            expected: 1,
                            got: arguments.len(),
                        });
                    }
                    self.expression(&arguments[0])?;
                    self.code.push(Op::QueueMicrotask);
                } else {
                    for argument in arguments {
                        self.expression(argument)?;
                    }
                    self.code
                        .push(Op::HostCall(callee.clone(), arguments.len()));
                }
            }
            Expr::CallValue { callee, arguments } => {
                self.expression(callee)?;
                for argument in arguments {
                    self.expression(argument)?;
                }
                self.code.push(Op::CallValue {
                    argc: arguments.len(),
                });
            }
            Expr::Lambda {
                parameters,
                body,
                min_arity,
            } => {
                let (index, upvalues) = self.compile_lambda(parameters, body, *min_arity)?;
                if upvalues.is_empty() {
                    // No captures: a plain function value, cheaper than a
                    // closure and identical in behaviour.
                    self.code.push(Op::Const(Value::Function(index)));
                } else {
                    // Load each captured value from the enclosing frame in
                    // upvalue order, then build the closure over them.
                    for upvalue in &upvalues {
                        self.code.push(Op::LoadLocal(upvalue.parent_slot));
                    }
                    self.code.push(Op::MakeClosure {
                        index,
                        upvalues: upvalues.len(),
                    });
                }
            }
            Expr::PostUpdate { name, delta } => {
                // Old value stays for the expression's result; Dup computes
                // the new value from a copy, Store writes it back (and
                // re-pushes it per its own contract), and the trailing Pop
                // discards that pushed copy so only the old value remains.
                if let Some((slot, constant)) = self.resolve(name) {
                    if constant {
                        return Err(JsError::AssignmentToConstant { name: name.clone() });
                    }
                    self.code.push(Op::LoadLocal(slot));
                    self.code.push(Op::Dup);
                    self.code.push(Op::Const(Value::Number(*delta)));
                    self.code.push(Op::Add);
                    self.code.push(Op::StoreLocal(slot));
                } else if let Some((slot, constant)) = self.global_slot(name) {
                    if constant {
                        return Err(JsError::AssignmentToConstant { name: name.clone() });
                    }
                    self.code.push(Op::LoadGlobal(slot));
                    self.code.push(Op::Dup);
                    self.code.push(Op::Const(Value::Number(*delta)));
                    self.code.push(Op::Add);
                    self.code.push(Op::StoreGlobal(slot));
                } else {
                    return Err(JsError::UndefinedVariable { name: name.clone() });
                }
                self.code.push(Op::Pop);
            }
            Expr::CompoundMember {
                object,
                key,
                operator,
                right,
            } => {
                // Object and key are compiled — and therefore evaluated —
                // exactly once each; Dup2 supplies the second (object, key)
                // pair GetProperty consumes to read the current value, so the
                // property's read and write share the same reference rather
                // than two independently evaluated ones. See the type's own
                // doc comment for why that distinction matters.
                self.expression(object)?;
                self.expression(key)?;
                self.code.push(Op::Dup2);
                self.code.push(Op::GetProperty);
                self.expression(right)?;
                self.code.push(match operator.as_str() {
                    "+" => Op::Add,
                    "-" => Op::Sub,
                    "*" => Op::Mul,
                    _ => Op::Div,
                });
                self.code.push(Op::SetProperty);
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

/// Parses `source` as a single, standalone expression — used to turn a
/// template literal interpolation's raw text (captured whole by
/// `scan_template_literal`, since the lexer has no AST to build it into)
/// into a real `Expr`. Refuses trailing content after the expression
/// rather than silently ignoring it, the same as `compile` refusing
/// anything `parse_program` cannot fully consume.
fn parse_expression_from_source(source: &str) -> Result<Expr, JsError> {
    // Strict, not tolerant — see `lex`'s own doc comment on
    // `tolerate_unknown`: this substring's tokens are the real program.
    let (tokens, starts) = lex(source, false)?;
    let mut parser = Parser::new(source, tokens, starts);
    let expression = parser.parse_expression()?;
    if !matches!(parser.peek(), Token::Eof) {
        return Err(JsError::UnexpectedToken {
            found: parser.peek().describe(),
            expected: "the end of the interpolation expression".to_string(),
        });
    }
    Ok(expression)
}

/// Compiles `source` into bytecode.
///
/// # Errors
///
/// Returns [`JsError`] for a lexical, syntactic, or unsupported-feature
/// condition. Unsupported features are refused here rather than at run time so
/// that a program which compiles can be trusted to mean what it says.
pub fn compile(source: &str) -> Result<Program, JsError> {
    // Tolerant: the one whole-file eager pass — see `lex`'s own doc
    // comment on `tolerate_unknown`.
    let (tokens, starts) = lex(source, true)?;
    let statements = Parser::new(source, tokens, starts).parse_program()?;
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
        if arguments.len() < function.min_arity || arguments.len() > function.arity {
            return Err(JsError::OperationArity {
                name: name.to_string(),
                // The lower bound would be more precise for a defaulted
                // function, but `OperationArity` reports a single expected
                // count everywhere else it's used (host-operation arity,
                // which never has defaults) — `arity` (the max) keeps this
                // one embedder-facing call site consistent with those
                // rather than growing a min/max shape only this call needs.
                expected: function.arity,
                got: arguments.len(),
            });
        }
        let mut runtime = Runtime::default();
        let result = self.run_function(program, index, arguments, &mut runtime, host)?;
        self.drain_microtasks(program, &mut runtime, host)?;
        Ok(result)
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
        let result = self.run_function(program, 0, Vec::new(), &mut runtime, host)?;
        self.drain_microtasks(program, &mut runtime, host)?;
        Ok(result)
    }

    /// Runs every queued microtask to completion, including ones a microtask
    /// itself queues, before returning control to the caller.
    ///
    /// This is the whole of what a microtask queue promises: work scheduled
    /// during a script's execution runs after that script finishes and
    /// before the caller regains control, in the order it was scheduled. One
    /// task at a time — never a batch snapshot — so a task queuing another
    /// sees it drained in this same flush rather than deferred to the next
    /// external call into the interpreter.
    ///
    /// # Errors
    ///
    /// Returns the first error any queued task produces. A microtask's
    /// failure is not swallowed and does not let the remaining queue run
    /// past it — this interpreter has no try/catch to isolate one task's
    /// exception from another's, and every other failure mode here already
    /// fails the whole call rather than continuing past a defect.
    fn drain_microtasks(
        &self,
        program: &Program,
        runtime: &mut Runtime,
        host: &mut dyn Host,
    ) -> Result<(), JsError> {
        while !runtime.microtasks.is_empty() {
            let task = runtime.microtasks.remove(0);
            let (index, captured) = match task {
                Value::Function(index) => (index, Vec::new()),
                Value::Closure(handle) => closure_parts(runtime, handle)?,
                // Op::QueueMicrotask type-checks before queuing; nothing else
                // ever reaches this vector.
                _ => continue,
            };
            self.run_function_with_upvalues(program, index, Vec::new(), &captured, runtime, host)?;
        }
        Ok(())
    }

    fn run_function(
        &self,
        program: &Program,
        index: usize,
        arguments: Vec<Value>,
        runtime: &mut Runtime,
        host: &mut dyn Host,
    ) -> Result<Value, JsError> {
        self.run_function_with_upvalues(program, index, arguments, &[], runtime, host)
    }

    /// Runs a function with a set of captured upvalue values.
    ///
    /// A plain function is called with no upvalues; a closure is called with
    /// the values it captured at creation. Because only `const` bindings are
    /// captured, these values are snapshots that cannot have gone stale — the
    /// binding they came from cannot have changed.
    fn run_function_with_upvalues(
        &self,
        program: &Program,
        index: usize,
        arguments: Vec<Value>,
        upvalues: &[Value],
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
                Op::LoadGlobal(slot) => {
                    stack.push(
                        runtime
                            .globals
                            .get(*slot)
                            .cloned()
                            .unwrap_or(Value::Undefined),
                    );
                }
                Op::StoreGlobal(slot) => {
                    let value = stack.last().cloned().unwrap_or(Value::Undefined);
                    if *slot >= runtime.globals.len() {
                        runtime.globals.resize(slot + 1, Value::Undefined);
                    }
                    runtime.globals[*slot] = value;
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
                Op::Dup2 => {
                    let len = stack.len();
                    // A well-formed program (the only kind this compiler
                    // emits) never reaches this op with fewer than two values
                    // present; `saturating_sub` keeps a malformed one a
                    // no-op read of `undefined` rather than a panic.
                    let base = len.saturating_sub(2);
                    let a = stack.get(base).cloned().unwrap_or(Value::Undefined);
                    let b = stack.get(base + 1).cloned().unwrap_or(Value::Undefined);
                    stack.push(a);
                    stack.push(b);
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
                Op::NewArray(count) => {
                    // Charged like an object plus one property per element, so
                    // a large literal cannot allocate unbilled.
                    let charge = OBJECT_OVERHEAD_BYTES
                        .saturating_add((*count as u64).saturating_mul(ELEMENT_OVERHEAD_BYTES));
                    runtime.bytes = runtime.bytes.saturating_add(charge);
                    if runtime.bytes > self.byte_limit {
                        return Err(JsError::ByteLimitExceeded {
                            limit: self.byte_limit,
                        });
                    }
                    if runtime.heap.occupied_slots() >= COLLECT_AFTER_ALLOCATIONS {
                        collect_now(runtime, &stack, &locals);
                    }
                    // Elements are on the stack with element 0 deepest; take
                    // them in order. Same hazard `Op::Dup2` documents: a
                    // well-formed program (the only kind this compiler
                    // emits) always pushed exactly `count` elements right
                    // before this op, so `stack.len() >= *count` always
                    // holds in practice — but `saturating_sub` costs nothing
                    // and keeps a malformed program a degraded read rather
                    // than a `panic = "abort"` release build taking the
                    // whole embedding process down with it.
                    let start = stack.len().saturating_sub(*count);
                    let elements: Vec<Value> = stack.split_off(start);
                    let mut data = ObjectData::default();
                    for (index, element) in elements.into_iter().enumerate() {
                        data.set(index.to_string(), element);
                    }
                    data.set("length".to_owned(), Value::Number(*count as f64));
                    let reference =
                        runtime
                            .heap
                            .allocate(data)
                            .map_err(|error| JsError::TypeError {
                                message: error.to_string(),
                            })?;
                    stack.push(Value::Array(reference));
                }
                Op::GetProperty => {
                    let key = pop(&mut stack);
                    let object = pop(&mut stack);
                    // A string has no heap object to look a stored property
                    // up in, but `.length` (and, in real JS, an unknown
                    // property reading `undefined` rather than refusing) are
                    // still real string behaviour. A string *method*
                    // (`.indexOf`, `.slice`, ...) is resolved separately, by
                    // `Op::CallMethod`, not through here — so an unrecognised
                    // key here (including a known method's own bare name,
                    // never called) reads `undefined`, matching every other
                    // "absence is ordinary" property read in this VM.
                    if let Value::String(text) = &object {
                        let value = if property_key(&key) == "length" {
                            Value::Number(text.chars().count() as f64)
                        } else {
                            Value::Undefined
                        };
                        stack.push(value);
                        pointer += 1;
                        continue;
                    }
                    let (Value::Object(handle) | Value::Array(handle)) = object else {
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
                    let is_array = matches!(object, Value::Array(_));
                    let (Value::Object(handle) | Value::Array(handle)) = object else {
                        return Err(JsError::TypeError {
                            message: format!("cannot access a property of {object}"),
                        });
                    };
                    let stored_key = property_key(&key);
                    // Writing `arr[i]` at or past the end grows `length`, which
                    // is the array behaviour a plain object does not have.
                    let grow_length = if is_array {
                        array_index(&stored_key).map(|index| u64::from(index) + 1)
                    } else {
                        None
                    };
                    let object =
                        runtime
                            .heap
                            .get_mut(handle)
                            .map_err(|error| JsError::TypeError {
                                message: error.to_string(),
                            })?;
                    let mut charged = object.set(stored_key, value.clone());
                    if let Some(new_length) = grow_length {
                        let current = object.get("length").map(to_number).unwrap_or(0.0);
                        #[allow(clippy::cast_precision_loss)]
                        if (new_length as f64) > current {
                            charged +=
                                object.set("length".to_owned(), Value::Number(new_length as f64));
                        }
                    }
                    runtime.bytes = runtime.bytes.saturating_add(charged as u64);
                    if runtime.bytes > self.byte_limit {
                        return Err(JsError::ByteLimitExceeded {
                            limit: self.byte_limit,
                        });
                    }
                    stack.push(value);
                }
                Op::DeleteProperty => {
                    let key = pop(&mut stack);
                    let object = pop(&mut stack);
                    let (Value::Object(handle) | Value::Array(handle)) = object else {
                        return Err(JsError::TypeError {
                            message: format!("cannot delete a property of {object}"),
                        });
                    };
                    let object =
                        runtime
                            .heap
                            .get_mut(handle)
                            .map_err(|error| JsError::TypeError {
                                message: error.to_string(),
                            })?;
                    object.remove(&property_key(&key));
                    stack.push(Value::Boolean(true));
                }
                Op::SpreadInto => {
                    let source = pop(&mut stack);
                    let target = pop(&mut stack);
                    // Matched on a reference, not moved, so `target` is
                    // still whole afterward to push back below.
                    let handle = match &target {
                        Value::Object(handle) | Value::Array(handle) => *handle,
                        _ => {
                            return Err(JsError::TypeError {
                                message: format!("cannot spread into {target}"),
                            });
                        }
                    };
                    // Real JS spreads own enumerable properties of an
                    // object/array and treats null/undefined as spreading
                    // nothing at all (`{...null}` is `{}`); anything else
                    // refuses rather than silently spreading nothing, so a
                    // real mistake (spreading a number, a function) is
                    // never mistaken for a legitimate no-op.
                    // A known, narrow divergence from real JS: an array's
                    // "length" is an ordinary entry in this engine's object
                    // model (no non-enumerable distinction exists), so
                    // spreading an array here also copies "length" onto the
                    // result, where real JS's non-enumerable length would
                    // not. Only reachable by spreading an array as an
                    // object source (`{...arr}`), which nothing in Nova
                    // does — flagged here rather than silently shipped.
                    let source_entries: Vec<(String, Value)> = match &source {
                        Value::Undefined | Value::Null => Vec::new(),
                        Value::Object(source_handle) | Value::Array(source_handle) => runtime
                            .heap
                            .get(*source_handle)
                            .map_err(|error| JsError::TypeError {
                                message: error.to_string(),
                            })?
                            .entries
                            .clone(),
                        other => {
                            return Err(JsError::TypeError {
                                message: format!("cannot spread {other}"),
                            });
                        }
                    };
                    let object =
                        runtime
                            .heap
                            .get_mut(handle)
                            .map_err(|error| JsError::TypeError {
                                message: error.to_string(),
                            })?;
                    let mut charged = 0u64;
                    for (key, value) in source_entries {
                        charged += object.set(key, value) as u64;
                    }
                    runtime.bytes = runtime.bytes.saturating_add(charged);
                    if runtime.bytes > self.byte_limit {
                        return Err(JsError::ByteLimitExceeded {
                            limit: self.byte_limit,
                        });
                    }
                    stack.push(target);
                }
                Op::ConstructRegex { argc } => {
                    let split = stack.len().saturating_sub(*argc);
                    let arguments = stack.split_off(split);
                    let pattern = match arguments.first() {
                        Some(Value::String(text)) => text.clone(),
                        other => {
                            return Err(JsError::TypeError {
                                message: format!(
                                    "new RegExp expects a string pattern, got {}",
                                    other
                                        .map_or_else(|| "nothing".to_string(), ToString::to_string)
                                ),
                            });
                        }
                    };
                    let flags = match arguments.get(1) {
                        Some(Value::String(text)) => text.clone(),
                        Some(other) => {
                            return Err(JsError::TypeError {
                                message: format!(
                                    "new RegExp expects a string flags argument, got {other}"
                                ),
                            });
                        }
                        None => String::new(),
                    };
                    let compiled = regex::compile_pattern(&pattern, &flags).map_err(|error| {
                        JsError::Unsupported {
                            feature: format!("the regular expression /{pattern}/{flags}: {error}"),
                        }
                    })?;
                    stack.push(Value::Regex(Rc::new(compiled)));
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
                Op::CallValue { argc } => {
                    let split = stack.len().saturating_sub(*argc);
                    let arguments = stack.split_off(split);
                    let callee = pop(&mut stack);
                    let result = self.call_function_value(
                        program, callee, arguments, &stack, &locals, runtime, host,
                    )?;
                    stack.push(result);
                }
                Op::MakeClosure { index, upvalues } => {
                    runtime.bytes =
                        runtime
                            .bytes
                            .saturating_add(OBJECT_OVERHEAD_BYTES.saturating_add(
                                (*upvalues as u64).saturating_mul(ELEMENT_OVERHEAD_BYTES),
                            ));
                    if runtime.bytes > self.byte_limit {
                        return Err(JsError::ByteLimitExceeded {
                            limit: self.byte_limit,
                        });
                    }
                    // Same hazard as `Op::NewArray` just above, same fix:
                    // `saturating_sub` rather than a subtraction that could
                    // underflow if a malformed program ever desynced the
                    // captured-upvalue count from what's actually on the
                    // stack.
                    let start = stack.len().saturating_sub(*upvalues);
                    let captured = stack.split_off(start);
                    if runtime.heap.occupied_slots() >= COLLECT_AFTER_ALLOCATIONS {
                        collect_now(runtime, &stack, &locals);
                    }
                    let handle = make_closure(runtime, *index, &captured)?;
                    stack.push(Value::Closure(handle));
                }
                Op::LoadUpvalue(slot) => {
                    stack.push(upvalues.get(*slot).cloned().unwrap_or(Value::Undefined));
                }
                Op::QueueMicrotask => {
                    let task = pop(&mut stack);
                    if !matches!(task, Value::Function(_) | Value::Closure(_)) {
                        return Err(JsError::TypeError {
                            message: format!("queueMicrotask expects a function, got {task}"),
                        });
                    }
                    runtime.microtasks.push(task);
                    stack.push(Value::Undefined);
                }
                Op::CallMethod { name, argc } => {
                    let split = stack.len().saturating_sub(*argc);
                    let arguments = stack.split_off(split);
                    let receiver = pop(&mut stack);
                    // An own property holding a function/closure wins over
                    // any built-in — the same own-property-shadows-prototype
                    // rule real JS follows, and how a stored callback prop
                    // that happens to share a name with a built-in method
                    // (rare, but not impossible) still calls correctly.
                    let own =
                        match &receiver {
                            Value::Object(handle) | Value::Array(handle) => {
                                let object = runtime.heap.get(*handle).map_err(|error| {
                                    JsError::TypeError {
                                        message: error.to_string(),
                                    }
                                })?;
                                object.get(name).cloned()
                            }
                            _ => None,
                        };
                    let result =
                        if let Some(callee @ (Value::Function(_) | Value::Closure(_))) = own {
                            self.call_function_value(
                                program, callee, arguments, &stack, &locals, runtime, host,
                            )?
                        } else {
                            self.call_builtin_method(
                                program, receiver, name, arguments, &stack, &locals, runtime, host,
                            )?
                        };
                    stack.push(result);
                }
                Op::Return => return Ok(pop(&mut stack)),
            }
            pointer += 1;
        }
        Ok(Value::Undefined)
    }

    /// Calls `callee` (must be a `Value::Function`/`Value::Closure`) with
    /// exactly `arguments`, refusing on an arity mismatch — the ordinary,
    /// strict call contract every other call site in this interpreter uses.
    /// Factored out of what was `Op::CallValue`'s own body, so `Op::CallMethod`'s
    /// own-property-is-callable path shares it rather than a second copy.
    #[allow(clippy::too_many_arguments)]
    fn call_function_value(
        &self,
        program: &Program,
        callee: Value,
        arguments: Vec<Value>,
        stack: &[Value],
        locals: &[Value],
        runtime: &mut Runtime,
        host: &mut dyn Host,
    ) -> Result<Value, JsError> {
        let (index, captured) = match callee {
            Value::Function(index) => (index, Vec::new()),
            Value::Closure(handle) => closure_parts(runtime, handle)?,
            other => {
                return Err(JsError::TypeError {
                    message: format!("{other} is not a function"),
                });
            }
        };
        let function = program
            .functions
            .get(index)
            .ok_or_else(|| JsError::TypeError {
                message: "call to an unknown function value".to_owned(),
            })?;
        if arguments.len() < function.min_arity || arguments.len() > function.arity {
            return Err(JsError::TypeError {
                message: format!(
                    "a function value expects {} argument(s), got {}",
                    arity_range(function.min_arity, function.arity),
                    arguments.len()
                ),
            });
        }
        let restore = runtime.outer.len();
        runtime.outer.extend(stack.iter().cloned());
        runtime.outer.extend(locals.iter().cloned());
        runtime.outer.extend(captured.iter().cloned());
        let outcome =
            self.run_function_with_upvalues(program, index, arguments, &captured, runtime, host);
        runtime.outer.truncate(restore);
        outcome
    }

    /// Calls a built-in method's own callback argument, adapting the
    /// argument count to the callback's declared arity the way real JS
    /// invocation always does: a parameter the callback did not declare is
    /// simply never passed, and one it declared but the caller did not
    /// supply reads `undefined`. `call_function_value` requires an exact
    /// match deliberately (a mismatch there is normally a real bug, not a
    /// convention) — this exists specifically for `array.map((item) => ...)`,
    /// where a callback legitimately declares fewer parameters than `map`
    /// conventionally passes (item, index).
    #[allow(clippy::too_many_arguments)]
    fn call_callback(
        &self,
        program: &Program,
        callee: Value,
        mut arguments: Vec<Value>,
        stack: &[Value],
        locals: &[Value],
        runtime: &mut Runtime,
        host: &mut dyn Host,
    ) -> Result<Value, JsError> {
        let (index, captured) = match callee {
            Value::Function(index) => (index, Vec::new()),
            Value::Closure(handle) => closure_parts(runtime, handle)?,
            other => {
                return Err(JsError::TypeError {
                    message: format!("{other} is not a function"),
                });
            }
        };
        let function = program
            .functions
            .get(index)
            .ok_or_else(|| JsError::TypeError {
                message: "call to an unknown function value".to_owned(),
            })?;
        arguments.resize(function.arity, Value::Undefined);
        let restore = runtime.outer.len();
        runtime.outer.extend(stack.iter().cloned());
        runtime.outer.extend(locals.iter().cloned());
        runtime.outer.extend(captured.iter().cloned());
        let outcome =
            self.run_function_with_upvalues(program, index, arguments, &captured, runtime, host);
        runtime.outer.truncate(restore);
        outcome
    }

    /// Allocates a new array from `elements`, charged and safepointed
    /// exactly like `Op::NewArray` — the same allocation, reached from a
    /// built-in method (`slice`, `split`, `map`, `filter`) instead of that
    /// opcode.
    fn allocate_array(
        &self,
        runtime: &mut Runtime,
        stack: &[Value],
        locals: &[Value],
        elements: Vec<Value>,
    ) -> Result<Value, JsError> {
        let count = elements.len();
        let charge = OBJECT_OVERHEAD_BYTES
            .saturating_add((count as u64).saturating_mul(ELEMENT_OVERHEAD_BYTES));
        runtime.bytes = runtime.bytes.saturating_add(charge);
        if runtime.bytes > self.byte_limit {
            return Err(JsError::ByteLimitExceeded {
                limit: self.byte_limit,
            });
        }
        if runtime.heap.occupied_slots() >= COLLECT_AFTER_ALLOCATIONS {
            // `elements` is about to be stored into the array this call is
            // building, but it isn't reachable from stack/locals/outer/
            // globals yet — without rooting it here, this exact collection
            // pass would free it before it's installed, leaving the new
            // array holding dangling handles.
            let restore = runtime.outer.len();
            runtime.outer.extend(elements.iter().cloned());
            collect_now(runtime, stack, locals);
            runtime.outer.truncate(restore);
        }
        let mut data = ObjectData::default();
        for (index, element) in elements.into_iter().enumerate() {
            data.set(index.to_string(), element);
        }
        data.set("length".to_owned(), Value::Number(count as f64));
        let reference = runtime
            .heap
            .allocate(data)
            .map_err(|error| JsError::TypeError {
                message: error.to_string(),
            })?;
        Ok(Value::Array(reference))
    }

    /// Dispatches a method call to a receiver with no matching own property:
    /// a fixed, real-usage-driven set of String and Array built-ins.
    /// Refuses with a typed error for any other receiver type or any
    /// unrecognised name — the same never-silently-wrong contract every
    /// other unimplemented-feature path in this interpreter keeps.
    #[allow(clippy::too_many_arguments)]
    fn call_builtin_method(
        &self,
        program: &Program,
        receiver: Value,
        name: &str,
        arguments: Vec<Value>,
        stack: &[Value],
        locals: &[Value],
        runtime: &mut Runtime,
        host: &mut dyn Host,
    ) -> Result<Value, JsError> {
        match receiver {
            Value::String(text) => {
                self.call_string_method(&text, name, &arguments, stack, locals, runtime)
            }
            Value::Array(handle) => self.call_array_method(
                program, handle, name, arguments, stack, locals, runtime, host,
            ),
            Value::Regex(regex) => call_regex_method(&regex, name, &arguments),
            other => Err(JsError::TypeError {
                message: format!("{other} has no method `{name}`"),
            }),
        }
    }

    fn call_string_method(
        &self,
        text: &str,
        name: &str,
        arguments: &[Value],
        stack: &[Value],
        locals: &[Value],
        runtime: &mut Runtime,
    ) -> Result<Value, JsError> {
        // Real `String.prototype.replace` takes a regex or a plain string
        // search. A regex search is refused here rather than silently
        // stringified into a literal substring match (which `arg_string`'s
        // `Display` fallback would otherwise do, matching `/pattern/flags`
        // as literal text — wrong, and silently so): every real use of
        // `.replace()` with a regex in Nova is the `g`-flag,
        // `$&`-backreference search-highlighter, whose statefulness this
        // milestone does not implement (see `mod regex`'s module doc
        // comment on what is deferred).
        if name == "replace" && matches!(arguments.first(), Some(Value::Regex(_))) {
            return Err(JsError::Unsupported {
                feature: "String.prototype.replace with a regular expression".to_string(),
            });
        }
        let arg_string = |i: usize| {
            arguments
                .get(i)
                .map(ToString::to_string)
                .unwrap_or_default()
        };
        match name {
            "indexOf" => {
                let needle = arg_string(0);
                let result = text
                    .find(needle.as_str())
                    .map(|byte| text[..byte].chars().count() as f64)
                    .unwrap_or(-1.0);
                Ok(Value::Number(result))
            }
            "includes" => Ok(Value::Boolean(text.contains(arg_string(0).as_str()))),
            "startsWith" => Ok(Value::Boolean(text.starts_with(arg_string(0).as_str()))),
            "toLowerCase" => Ok(Value::String(text.to_lowercase())),
            "toUpperCase" => Ok(Value::String(text.to_uppercase())),
            "trim" => Ok(Value::String(text.trim().to_string())),
            // A plain-string search replaces only the first occurrence —
            // real JS's own behavior when the search argument is a string
            // rather than a `/g`-flagged regex (refused above, before this
            // match, rather than reaching here).
            "replace" => Ok(Value::String(text.replacen(
                arg_string(0).as_str(),
                arg_string(1).as_str(),
                1,
            ))),
            "slice" => {
                let chars: Vec<char> = text.chars().collect();
                let len = chars.len() as i64;
                let start = arguments
                    .first()
                    .map(to_number)
                    .map(|n| clamp_slice_index(n, len))
                    .unwrap_or(0);
                let end = arguments
                    .get(1)
                    .map(to_number)
                    .map(|n| clamp_slice_index(n, len))
                    .unwrap_or(len);
                let (start, end) = (start.max(0) as usize, end.max(0) as usize);
                let sliced = if start < end {
                    chars[start.min(chars.len())..end.min(chars.len())]
                        .iter()
                        .collect()
                } else {
                    String::new()
                };
                Ok(Value::String(sliced))
            }
            "split" => {
                let separator = arg_string(0);
                let pieces: Vec<Value> = if separator.is_empty() {
                    text.chars().map(|c| Value::String(c.to_string())).collect()
                } else {
                    text.split(separator.as_str())
                        .map(|piece| Value::String(piece.to_string()))
                        .collect()
                };
                self.allocate_array(runtime, stack, locals, pieces)
            }
            _ => Err(JsError::TypeError {
                message: format!("a string has no method `{name}`"),
            }),
        }
    }

    #[allow(clippy::too_many_arguments)]
    fn call_array_method(
        &self,
        program: &Program,
        handle: GcRef,
        name: &str,
        arguments: Vec<Value>,
        stack: &[Value],
        locals: &[Value],
        runtime: &mut Runtime,
        host: &mut dyn Host,
    ) -> Result<Value, JsError> {
        match name {
            "push" => {
                let mut elements = array_elements(runtime, handle)?;
                elements.extend(arguments);
                let new_length = elements.len();
                let object = runtime
                    .heap
                    .get_mut(handle)
                    .map_err(|error| JsError::TypeError {
                        message: error.to_string(),
                    })?;
                for (index, element) in elements.into_iter().enumerate() {
                    object.set(index.to_string(), element);
                }
                object.set("length".to_owned(), Value::Number(new_length as f64));
                Ok(Value::Number(new_length as f64))
            }
            "join" => {
                let elements = array_elements(runtime, handle)?;
                let separator = arguments
                    .first()
                    .map(ToString::to_string)
                    .unwrap_or_else(|| ",".to_string());
                let joined = elements
                    .iter()
                    .map(|value| match value {
                        Value::Undefined | Value::Null => String::new(),
                        other => other.to_string(),
                    })
                    .collect::<Vec<_>>()
                    .join(&separator);
                Ok(Value::String(joined))
            }
            "indexOf" => {
                let elements = array_elements(runtime, handle)?;
                let needle = arguments.first().cloned().unwrap_or(Value::Undefined);
                let result = elements
                    .iter()
                    .position(|value| strict_equal(value, &needle))
                    .map(|index| index as f64)
                    .unwrap_or(-1.0);
                Ok(Value::Number(result))
            }
            "includes" => {
                let elements = array_elements(runtime, handle)?;
                let needle = arguments.first().cloned().unwrap_or(Value::Undefined);
                Ok(Value::Boolean(
                    elements.iter().any(|value| strict_equal(value, &needle)),
                ))
            }
            "slice" => {
                let elements = array_elements(runtime, handle)?;
                let len = elements.len() as i64;
                let start = arguments
                    .first()
                    .map(to_number)
                    .map(|n| clamp_slice_index(n, len))
                    .unwrap_or(0);
                let end = arguments
                    .get(1)
                    .map(to_number)
                    .map(|n| clamp_slice_index(n, len))
                    .unwrap_or(len);
                let sliced = if start < end {
                    elements[start as usize..end as usize].to_vec()
                } else {
                    Vec::new()
                };
                self.allocate_array(runtime, stack, locals, sliced)
            }
            "map" | "filter" | "forEach" | "find" | "findIndex" | "some" => {
                let elements = array_elements(runtime, handle)?;
                let callback = arguments
                    .first()
                    .cloned()
                    .ok_or_else(|| JsError::TypeError {
                        message: format!("{name} requires a callback argument"),
                    })?;
                // `elements` and the Rust-side accumulator each method
                // builds up (`mapped`/`kept`) live outside stack/locals for
                // the whole loop — `collect_now` cannot see them on its
                // own. Any one callback call below may allocate enough
                // inside its own body to cross the collection threshold, so
                // the not-yet-visited elements plus everything accumulated
                // so far are rooted via `runtime.outer` around every call
                // and un-rooted right after, mirroring how `call_callback`
                // already roots its own frame.
                match name {
                    "map" => {
                        let mut mapped: Vec<Value> = Vec::with_capacity(elements.len());
                        for index in 0..elements.len() {
                            let args = vec![elements[index].clone(), Value::Number(index as f64)];
                            let restore = runtime.outer.len();
                            runtime.outer.extend(elements[index..].iter().cloned());
                            runtime.outer.extend(mapped.iter().cloned());
                            let result = self.call_callback(
                                program,
                                callback.clone(),
                                args,
                                stack,
                                locals,
                                runtime,
                                host,
                            );
                            runtime.outer.truncate(restore);
                            mapped.push(result?);
                        }
                        self.allocate_array(runtime, stack, locals, mapped)
                    }
                    "filter" => {
                        let mut kept: Vec<Value> = Vec::new();
                        for index in 0..elements.len() {
                            let element = elements[index].clone();
                            let args = vec![element.clone(), Value::Number(index as f64)];
                            let restore = runtime.outer.len();
                            runtime.outer.extend(elements[index..].iter().cloned());
                            runtime.outer.extend(kept.iter().cloned());
                            let keep = self.call_callback(
                                program,
                                callback.clone(),
                                args,
                                stack,
                                locals,
                                runtime,
                                host,
                            );
                            runtime.outer.truncate(restore);
                            if keep?.truthy() {
                                kept.push(element);
                            }
                        }
                        self.allocate_array(runtime, stack, locals, kept)
                    }
                    "forEach" => {
                        for index in 0..elements.len() {
                            let args = vec![elements[index].clone(), Value::Number(index as f64)];
                            let restore = runtime.outer.len();
                            runtime.outer.extend(elements[index..].iter().cloned());
                            let result = self.call_callback(
                                program,
                                callback.clone(),
                                args,
                                stack,
                                locals,
                                runtime,
                                host,
                            );
                            runtime.outer.truncate(restore);
                            result?;
                        }
                        Ok(Value::Undefined)
                    }
                    "find" => {
                        for index in 0..elements.len() {
                            let element = elements[index].clone();
                            let args = vec![element.clone(), Value::Number(index as f64)];
                            let restore = runtime.outer.len();
                            runtime.outer.extend(elements[index..].iter().cloned());
                            let matched = self.call_callback(
                                program,
                                callback.clone(),
                                args,
                                stack,
                                locals,
                                runtime,
                                host,
                            );
                            runtime.outer.truncate(restore);
                            if matched?.truthy() {
                                return Ok(element);
                            }
                        }
                        Ok(Value::Undefined)
                    }
                    "findIndex" => {
                        for index in 0..elements.len() {
                            let args = vec![elements[index].clone(), Value::Number(index as f64)];
                            let restore = runtime.outer.len();
                            runtime.outer.extend(elements[index..].iter().cloned());
                            let matched = self.call_callback(
                                program,
                                callback.clone(),
                                args,
                                stack,
                                locals,
                                runtime,
                                host,
                            );
                            runtime.outer.truncate(restore);
                            if matched?.truthy() {
                                return Ok(Value::Number(index as f64));
                            }
                        }
                        Ok(Value::Number(-1.0))
                    }
                    "some" => {
                        for index in 0..elements.len() {
                            let args = vec![elements[index].clone(), Value::Number(index as f64)];
                            let restore = runtime.outer.len();
                            runtime.outer.extend(elements[index..].iter().cloned());
                            let matched = self.call_callback(
                                program,
                                callback.clone(),
                                args,
                                stack,
                                locals,
                                runtime,
                                host,
                            );
                            runtime.outer.truncate(restore);
                            if matched?.truthy() {
                                return Ok(Value::Boolean(true));
                            }
                        }
                        Ok(Value::Boolean(false))
                    }
                    _ => unreachable!("matched above"),
                }
            }
            "reduce" => {
                let elements = array_elements(runtime, handle)?;
                let callback = arguments
                    .first()
                    .cloned()
                    .ok_or_else(|| JsError::TypeError {
                        message: "reduce requires a callback argument".to_string(),
                    })?;
                let mut index = 0usize;
                let mut accumulator = if let Some(initial) = arguments.get(1) {
                    initial.clone()
                } else {
                    let Some(first) = elements.first().cloned() else {
                        return Err(JsError::TypeError {
                            message: "reduce of empty array with no initial value".to_string(),
                        });
                    };
                    index = 1;
                    first
                };
                while index < elements.len() {
                    let args = vec![
                        accumulator.clone(),
                        elements[index].clone(),
                        Value::Number(index as f64),
                    ];
                    // Roots both the not-yet-visited elements and the
                    // in-flight accumulator — same reasoning as the
                    // map/filter/etc. loop above.
                    let restore = runtime.outer.len();
                    runtime.outer.extend(elements[index..].iter().cloned());
                    runtime.outer.push(accumulator.clone());
                    let result = self.call_callback(
                        program,
                        callback.clone(),
                        args,
                        stack,
                        locals,
                        runtime,
                        host,
                    );
                    runtime.outer.truncate(restore);
                    accumulator = result?;
                    index += 1;
                }
                Ok(accumulator)
            }
            _ => Err(JsError::TypeError {
                message: format!("an array has no method `{name}`"),
            }),
        }
    }
}

/// Dispatches a method call to a `Value::Regex` receiver.
///
/// Only `.test()` is implemented. `.exec()` and the stateful `lastIndex`/
/// global-iteration protocol real usage also needs (see the
/// `turing-nova-source-real-scope` project memory) are Milestone 2+ work —
/// they matter once a script actually iterates, which a static first paint
/// never does — and are refused here rather than approximated.
fn call_regex_method(
    regex: &regex::CompiledRegex,
    name: &str,
    arguments: &[Value],
) -> Result<Value, JsError> {
    match name {
        "test" => {
            let haystack = arguments
                .first()
                .map(ToString::to_string)
                .unwrap_or_default();
            Ok(Value::Boolean(regex::test(regex, &haystack)))
        }
        _ => Err(JsError::TypeError {
            message: format!("a regular expression has no method `{name}`"),
        }),
    }
}

/// Reads an array's elements in index order, `0..length`.
fn array_elements(runtime: &Runtime, handle: GcRef) -> Result<Vec<Value>, JsError> {
    let object = runtime
        .heap
        .get(handle)
        .map_err(|error| JsError::TypeError {
            message: error.to_string(),
        })?;
    let length = object.get("length").map(to_number).unwrap_or(0.0).max(0.0) as usize;
    Ok((0..length)
        .map(|index| {
            object
                .get(&index.to_string())
                .cloned()
                .unwrap_or(Value::Undefined)
        })
        .collect())
}

/// Clamps a `slice`-style index argument to `0..=len`: negative counts from
/// the end (`-1` is the last element), out of range clamps rather than
/// wraps or errors, `NaN` reads as `0` — the same coercion
/// `String.prototype.slice`/`Array.prototype.slice` use in real JS.
fn clamp_slice_index(n: f64, len: i64) -> i64 {
    if n.is_nan() {
        return 0;
    }
    let n = n as i64;
    let n = if n < 0 { (len + n).max(0) } else { n };
    n.min(len)
}

fn pop(stack: &mut Vec<Value>) -> Value {
    stack.pop().unwrap_or(Value::Undefined)
}

/// Allocates a closure object: the function index plus the captured values.
///
/// Stored in the ordinary object heap so the collector already traces the
/// captured values through it. The bookkeeping keys `"fn"` and `"n"` cannot
/// collide with the numeric element keys.
fn make_closure(runtime: &mut Runtime, index: usize, captured: &[Value]) -> Result<GcRef, JsError> {
    let mut data = ObjectData::default();
    #[allow(clippy::cast_precision_loss)]
    data.set("fn".to_owned(), Value::Number(index as f64));
    #[allow(clippy::cast_precision_loss)]
    data.set("n".to_owned(), Value::Number(captured.len() as f64));
    for (slot, value) in captured.iter().enumerate() {
        data.set(slot.to_string(), value.clone());
    }
    runtime
        .heap
        .allocate(data)
        .map_err(|error| JsError::TypeError {
            message: error.to_string(),
        })
}

/// Reads a closure object back into a function index and its captured values.
fn closure_parts(runtime: &Runtime, handle: GcRef) -> Result<(usize, Vec<Value>), JsError> {
    let data = runtime
        .heap
        .get(handle)
        .map_err(|error| JsError::TypeError {
            message: error.to_string(),
        })?;
    let index = data.get("fn").map(to_number).unwrap_or(f64::NAN);
    let count = data.get("n").map(to_number).unwrap_or(0.0);
    #[allow(clippy::cast_possible_truncation, clippy::cast_sign_loss)]
    let (index, count) = (index as usize, count as usize);
    let captured = (0..count)
        .map(|slot| {
            data.get(&slot.to_string())
                .cloned()
                .unwrap_or(Value::Undefined)
        })
        .collect();
    Ok((index, captured))
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
    // Queued microtasks are live even though no frame currently references
    // them: a closure sitting in the queue is exactly as reachable as one on
    // the stack, and a collection between queuing and draining must not free
    // it out from under the later call.
    let live = runtime
        .outer
        .iter()
        .chain(stack)
        .chain(locals)
        .chain(&runtime.globals)
        .chain(&runtime.microtasks)
        .filter_map(|value| match value {
            Value::Object(reference) | Value::Array(reference) | Value::Closure(reference) => {
                Some(*reference)
            }
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
    /// Top-level `const`/`let`/`var` bindings, addressed by
    /// [`Op::LoadGlobal`]/[`Op::StoreGlobal`] and shared by every call frame
    /// for the lifetime of one [`Vm::run_with_host`]/[`Vm::call`]. Grows
    /// lazily to the highest slot stored so far, the same convention
    /// `locals` in each frame already uses.
    globals: Vec<Value>,
    steps: u64,
    bytes: u64,
    /// Functions and closures queued by `queueMicrotask`, FIFO. Drained after
    /// the currently running top-level call finishes, in [`Vm::call`] and
    /// [`Vm::run_with_host`] — the minimal event-loop primitive a runtime
    /// needs to schedule work after the synchronous script that triggered it
    /// returns, rather than during it.
    microtasks: Vec<Value>,
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

/// The charge per array element, on top of the array's object overhead.
const ELEMENT_OVERHEAD_BYTES: u64 = 16;

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
        // An object or array would coerce through `valueOf`/`toString`, which
        // needs a prototype chain this implementation does not model, so it is
        // NaN rather than a guessed conversion. A regex has no numeric
        // coercion in real JS either.
        Value::Undefined
        | Value::Function(_)
        | Value::Object(_)
        | Value::Array(_)
        | Value::Closure(_)
        | Value::Regex(_) => f64::NAN,
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
        // Two regex values are `===` only when they are the very same
        // literal's/`new RegExp` call's result, matching real JS (two
        // regexes with identical source/flags but different identities are
        // not `===`).
        (Value::Regex(a), Value::Regex(b)) => Rc::ptr_eq(a, b),
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

    /// Evaluates `body` (statements ending in a `return`) inside a function
    /// and returns its value. The top level discards completion values, so a
    /// value test needs a call frame.
    fn eval_in_fn(body: &str) -> Value {
        let program = compile(&format!("function main() {{ {body} }} main();")).expect("compiles");
        Vm::default()
            .call(&program, "main", Vec::new(), &mut NoHost::default())
            .expect("runs")
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
    fn ternary_conditional_evaluates_the_taken_branch() {
        assert_eq!(expr("true ? 1 : 2"), Value::Number(1.0));
        assert_eq!(expr("false ? 1 : 2"), Value::Number(2.0));
        // A real Nova shape: `i === -1 ? url : url.slice(0, i)`.
        assert_eq!(
            eval_in_fn(
                "let i = -1; let url = \"example.com\"; \
                 return i === -1 ? url : \"unreachable\";"
            ),
            Value::String("example.com".to_string())
        );
        // Right-associative chaining: `a ? b : c ? d : e` reads as
        // `a ? b : (c ? d : e)`.
        assert_eq!(expr("false ? 1 : true ? 2 : 3"), Value::Number(2.0));
        assert_eq!(expr("false ? 1 : false ? 2 : 3"), Value::Number(3.0));
        // Usable as a value: assigned, returned, and as a call argument.
        assert_eq!(
            eval_in_fn("let x = 5 > 3 ? \"big\" : \"small\"; return x;"),
            Value::String("big".to_string())
        );
    }

    #[test]
    fn ternary_conditional_does_not_evaluate_the_untaken_branch() {
        let program = compile(
            "function main() { \
                true ? record(1) : record(2); \
                false ? record(3) : record(4); \
             } main();",
        )
        .expect("compiles");
        let mut host = RecordingHost::new();
        Vm::default()
            .run_with_host(&program, &mut host)
            .expect("runs");
        assert_eq!(
            host.calls,
            vec![1.0, 4.0],
            "only the taken branch of each ternary should have run"
        );
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
    fn a_trailing_default_parameter_applies_only_when_the_argument_is_omitted() {
        // The real Nova shapes: `function useVirtual(ref, rowH, count, over
        // = 6) {}` called as `useVirtual(ref, ROW, list.length)` (one fewer
        // argument than declared), and `useCallback((clr = "ac") => {...})`
        // called as `sweep()` (zero arguments). A named call short of the
        // full parameter count is no longer a compile-time arity refusal
        // when the missing parameters all have defaults. Declared at the
        // top level, not nested in `main`, since nested function
        // declarations are their own separate refusal.
        fn call(source: &str) -> Value {
            let program = compile(source).expect("compiles");
            Vm::default()
                .call(&program, "main", Vec::new(), &mut NoHost::default())
                .expect("runs")
        }
        assert_eq!(
            call(
                "function withDefault(a, b, over = 6) { return a + b + over; } \
                 function main() { return withDefault(1, 2); }"
            ),
            Value::Number(9.0)
        );
        // An explicit argument is kept — even a falsy one — never
        // overridden by the default (`apply_pattern_default`'s `===
        // undefined` check, not a truthiness check).
        assert_eq!(
            call(
                "function withDefault(a, b, over = 6) { return a + b + over; } \
                 function main() { return withDefault(1, 2, 0); }"
            ),
            Value::Number(3.0),
            "an explicit 0 must not be replaced by the default"
        );
        assert_eq!(
            call(
                "function withDefault(a, b, over = 6) { return a + b + over; } \
                 function main() { return withDefault(1, 2, 100); }"
            ),
            Value::Number(103.0)
        );
    }

    #[test]
    fn a_default_parameter_on_an_arrow_function_value_applies_the_same_way() {
        // `sweep()` calls through `Op::CallValue`, not the named-call path
        // `a_trailing_default_parameter_applies_only_when_the_argument_is_
        // omitted` exercises — a distinct compile-time check and a distinct
        // runtime check (`call_function_value`) both need the same range.
        assert_eq!(
            eval_in_fn("let sweep = (clr = \"ac\") => clr; return sweep();"),
            Value::String("ac".to_string())
        );
        assert_eq!(
            eval_in_fn("let sweep = (clr = \"ac\") => clr; return sweep(\"other\");"),
            Value::String("other".to_string())
        );
    }

    #[test]
    fn a_call_below_the_minimum_or_above_the_maximum_arity_still_refuses() {
        // A defaulted parameter narrows the exact-match check to a range —
        // it must not remove it. Below `min_arity` (omitting a required,
        // non-defaulted parameter) and above `arity` (an extra argument
        // past the last declared parameter, defaulted or not) both still
        // refuse, the same as `wrong_argument_count_is_refused` already
        // proves for a function with no defaults at all.
        assert!(matches!(
            compile(
                "function f(a, b, over = 6) { return a; } function main() { return f(1); } main();"
            ),
            Err(JsError::TypeError { .. })
        ));
        assert!(matches!(
            compile(
                "function f(a, over = 6) { return a; } \
                 function main() { return f(1, 2, 3); } main();"
            ),
            Err(JsError::TypeError { .. })
        ));
    }

    #[test]
    fn vm_call_the_embedder_entry_point_also_honours_default_parameters() {
        // `Op::Call`/`Op::CallValue` (the two paths a script's own calls
        // take) are covered above; `Vm::call` is the third, separate arity
        // check — the embedder-facing entry point (how `turing-engine`
        // invokes `Nova()`/an event handler by name from outside the
        // script). It must accept a short call the same way.
        let program =
            compile("function withDefault(a, over = 6) { return a + over; }").expect("compiles");
        assert_eq!(
            Vm::default()
                .call(
                    &program,
                    "withDefault",
                    vec![Value::Number(1.0)],
                    &mut NoHost::default(),
                )
                .expect("runs"),
            Value::Number(7.0)
        );
    }

    #[test]
    fn a_parameter_after_a_default_parameter_is_refused() {
        // Real usage only ever has a default parameter last — non-trailing
        // defaults are a real, rarer JS shape this engine does not model,
        // refused rather than mishandled.
        assert!(matches!(
            compile("function f(a = 1, b) { return a + b; }"),
            Err(JsError::Unsupported { .. })
        ));
        assert!(matches!(
            compile("function f(a = 1, [b, c]) { return a; }"),
            Err(JsError::Unsupported { .. })
        ));
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
    fn arrays_index_and_carry_length() {
        // Literal, index access, and length.
        assert_eq!(
            eval_in_fn("let a = [10, 20, 30]; return a[1];"),
            Value::Number(20.0)
        );
        assert_eq!(
            eval_in_fn("let a = [10, 20, 30]; return a.length;"),
            Value::Number(3.0)
        );
        assert_eq!(
            eval_in_fn("let a = []; return a.length;"),
            Value::Number(0.0)
        );
        // Out-of-range read is undefined, per the specification.
        assert_eq!(eval_in_fn("let a = [1]; return a[5];"), Value::Undefined);
        // Writing past the end grows length.
        assert_eq!(
            eval_in_fn("let a = [1]; a[3] = 9; return a.length;"),
            Value::Number(4.0)
        );
        assert_eq!(
            eval_in_fn("let a = [1]; a[3] = 9; return a[3];"),
            Value::Number(9.0)
        );
        // Nested arrays and objects interoperate.
        assert_eq!(
            eval_in_fn("let a = [[1, 2], {v: 7}]; return a[0][1];"),
            Value::Number(2.0)
        );
        assert_eq!(
            eval_in_fn("let a = [[1, 2], {v: 7}]; return a[1].v;"),
            Value::Number(7.0)
        );
        // An array is truthy even when empty.
        assert_eq!(
            eval_in_fn("let a = []; if (a) { return 1; } else { return 0; }"),
            Value::Number(1.0)
        );
    }

    #[test]
    fn function_expressions_are_first_class_values() {
        // Stored in a local and called indirectly.
        assert_eq!(
            eval_in_fn("let f = function(x) { return x + 1; }; return f(41);"),
            Value::Number(42.0)
        );
        // Stored in an array and called through an index.
        assert_eq!(
            eval_in_fn("let fs = [function() { return 7; }]; return fs[0]();"),
            Value::Number(7.0)
        );
        // Passed to a declared higher-order function and invoked there.
        let program = compile(
            "function apply(g, v) { return g(v); } \
             function main() { let double = function(n) { return n + n; }; return apply(double, 21); } \
             main();",
        )
        .expect("compiles");
        assert_eq!(
            Vm::default()
                .call(&program, "main", Vec::new(), &mut NoHost::default())
                .expect("runs"),
            Value::Number(42.0)
        );
        // Returned from a function and then called.
        let program = compile(
            "function make() { return function() { return 99; }; } \
             function main() { let g = make(); return g(); } \
             main();",
        )
        .expect("compiles");
        assert_eq!(
            Vm::default()
                .call(&program, "main", Vec::new(), &mut NoHost::default())
                .expect("runs"),
            Value::Number(99.0)
        );
    }

    #[test]
    fn a_function_value_carries_the_right_arity_and_type_checks() {
        // Wrong argument count is a type error, like a named call.
        let program = compile(
            "function main() { let f = function(x) { return x; }; return f(1, 2); } main();",
        );
        // Arity mismatch on an indirect call is caught at runtime.
        if let Ok(program) = program {
            let result = Vm::default().call(&program, "main", Vec::new(), &mut NoHost::default());
            assert!(matches!(result, Err(JsError::TypeError { .. })));
        }
        // Calling a non-function is a type error.
        let program =
            compile("function main() { let x = 5; return x(); } main();").expect("compiles");
        assert!(matches!(
            Vm::default().call(&program, "main", Vec::new(), &mut NoHost::default()),
            Err(JsError::TypeError { .. })
        ));
    }

    #[test]
    fn a_closure_captures_an_enclosing_const_by_value() {
        // The inner function reads a `const` from the enclosing scope. Because
        // a const cannot change, the captured snapshot is correct for all time
        // — this is a real closure for the safe case.
        let program = compile(
            "function main() { \
                const base = 100; \
                let add = function(x) { return base + x; }; \
                return add(23); \
             } main();",
        )
        .expect("compiles");
        assert_eq!(
            Vm::default()
                .call(&program, "main", Vec::new(), &mut NoHost::default())
                .expect("runs"),
            Value::Number(123.0)
        );
    }

    #[test]
    fn a_returned_closure_still_sees_its_captured_const() {
        // The closure outlives the frame that created it; its captured const
        // is carried with it.
        let program = compile(
            "function adder(n) { const captured = n; return function(x) { return captured + x; }; } \
             function main() { let add10 = adder(10); return add10(5); } \
             main();",
        )
        .expect("compiles");
        assert_eq!(
            Vm::default()
                .call(&program, "main", Vec::new(), &mut NoHost::default())
                .expect("runs"),
            Value::Number(15.0)
        );
    }

    #[test]
    fn capturing_a_mutable_binding_is_refused_not_computed_wrong() {
        // A `let` can be reassigned, so a by-value snapshot could be wrong.
        // Rather than capture it incorrectly, the engine refuses — the whole
        // point of the const-only boundary.
        let source = "function main() { \
            let n = 10; \
            let f = function() { return n; }; \
            return f(); \
        } main();";
        assert!(matches!(compile(source), Err(JsError::Unsupported { .. })));
    }

    #[test]
    fn a_deeply_nested_lambda_reads_a_top_level_const_beyond_the_single_upvalue_level() {
        // `capturing_a_mutable_binding_is_refused_not_computed_wrong` above
        // documents the single-level, const-only upvalue restriction for a
        // *lexically enclosing* function. A top-level binding is a different
        // thing entirely — real script scope, not a capture — so it must
        // stay reachable no matter how many lambdas are nested in between.
        // Before the global table existed, a top-level `Stmt::Function`
        // body compiled with no enclosing scope at all, so even one level of
        // reference from inside `main` was an `UndefinedVariable` refusal.
        //
        // `record(..)` observes the result rather than a `Vm::call` return
        // value, because calling `main` directly by name (as most tests in
        // this file do) skips the top-level statements entirely — and it is
        // exactly those top-level statements that initialise `BASE`. Only
        // `run_with_host`, which runs the whole program starting at the top
        // level, exercises that initialisation.
        let program = compile(
            "const BASE = 10; \
             function main() { \
                let inner = function() { \
                    let innermost = function() { return BASE + 5; }; \
                    return innermost(); \
                }; \
                record(inner()); \
             } main();",
        )
        .expect("compiles");
        let mut host = RecordingHost::new();
        Vm::default()
            .run_with_host(&program, &mut host)
            .expect("runs");
        assert_eq!(host.calls, vec![15.0]);
    }

    #[test]
    fn a_top_level_function_is_referenced_by_value_not_only_called_directly() {
        // The pattern a JSX `<Component/>` desugar needs: the callee is
        // `Expr::Variable("Greet")`, not `Expr::Call { callee: "Greet", .. }`
        // — a plain reference to a sibling top-level declaration, stored and
        // invoked indirectly rather than named at the call site.
        let program = compile(
            "function Greet(name) { return \"hi \" + name; } \
             function main() { let g = Greet; return g(\"Ada\"); } \
             main();",
        )
        .expect("compiles");
        assert_eq!(
            Vm::default()
                .call(&program, "main", Vec::new(), &mut NoHost::default())
                .expect("runs"),
            Value::String("hi Ada".to_string())
        );
    }

    #[test]
    fn a_top_level_let_mutated_from_a_nested_function_call_is_visible_afterward() {
        // Real global storage, not a snapshot: three separate calls into
        // `bump`, each from `main`, each seeing the previous call's write.
        let program = compile(
            "let counter = 0; \
             function bump() { counter = counter + 1; } \
             function main() { bump(); bump(); bump(); record(counter); } \
             main();",
        )
        .expect("compiles");
        let mut host = RecordingHost::new();
        Vm::default()
            .run_with_host(&program, &mut host)
            .expect("runs");
        assert_eq!(host.calls, vec![3.0]);
    }

    #[test]
    fn a_top_level_let_is_post_incremented_from_a_nested_function() {
        let program = compile(
            "let n = 0; \
             function inc() { n++; } \
             function main() { inc(); inc(); record(n); } \
             main();",
        )
        .expect("compiles");
        let mut host = RecordingHost::new();
        Vm::default()
            .run_with_host(&program, &mut host)
            .expect("runs");
        assert_eq!(host.calls, vec![2.0]);
    }

    #[test]
    fn reassigning_a_top_level_const_from_a_nested_function_is_refused_at_compile_time() {
        let source = "const LOCKED = 1; \
             function tryMutate() { LOCKED = 2; } \
             tryMutate();";
        assert!(matches!(
            compile(source),
            Err(JsError::AssignmentToConstant { .. })
        ));
    }

    #[test]
    fn arrow_functions_are_sugar_for_function_values() {
        // Single param, expression body.
        assert_eq!(
            eval_in_fn("let inc = x => x + 1; return inc(41);"),
            Value::Number(42.0)
        );
        // Parenthesised params, expression body.
        assert_eq!(
            eval_in_fn("let add = (a, b) => a + b; return add(40, 2);"),
            Value::Number(42.0)
        );
        // No params.
        assert_eq!(
            eval_in_fn("let answer = () => 42; return answer();"),
            Value::Number(42.0)
        );
        // Block body with an explicit return.
        assert_eq!(
            eval_in_fn("let f = x => { let y = x * 2; return y; }; return f(21);"),
            Value::Number(42.0)
        );
        // Passed inline to a higher-order function.
        let program = compile(
            "function apply(g, v) { return g(v); } \
             function main() { return apply(n => n + n, 21); } \
             main();",
        )
        .expect("compiles");
        assert_eq!(
            Vm::default()
                .call(&program, "main", Vec::new(), &mut NoHost::default())
                .expect("runs"),
            Value::Number(42.0)
        );
    }

    #[test]
    fn array_destructuring_binds_each_element_in_order() {
        // The single most common shape in real Nova source: hook calls are
        // *always* written `const [x, setX] = useState(...)`.
        assert_eq!(
            eval_in_fn("const [a, b] = [1, 2]; return a + b;"),
            Value::Number(3.0)
        );
    }

    #[test]
    fn top_level_destructuring_creates_real_global_bindings() {
        // Destructuring at the very top level (outside any function body)
        // desugars to `Stmt::Sequence` the same way it does inside one —
        // but the top-level compile pass has its own separate handling for
        // turning a `Stmt::Declare` into a *global* store (so it stays
        // visible from any function, at any depth), and that handling did
        // not originally know to look inside a `Stmt::Sequence` at all:
        // the binding fell through to the ordinary per-scope-local
        // compiler instead, silently leaving its (correctly reserved)
        // global slot permanently `undefined`. A function reading the
        // binding by name — the only way a real program would ever
        // observe it — is what catches that; reading it back in the same
        // top-level scope the declaration ran in would not, since the
        // stray local slot happens to hold the right value there too.
        let program = compile(
            "const [a, b] = [10, 20]; \
             function main() { record(a + b); } main();",
        )
        .expect("compiles");
        let mut host = RecordingHost::new();
        Vm::default()
            .run_with_host(&program, &mut host)
            .expect("runs");
        assert_eq!(host.calls, vec![30.0]);
    }

    #[test]
    fn array_destructuring_skips_elided_slots() {
        // A real observed Nova shape: `const [, n, from] = c;` and
        // `const [g, t, s, , dest] = c;` — a hole binds nothing at that
        // position rather than being a parse error or consuming a name.
        assert_eq!(
            eval_in_fn("const [, n, from] = [1, 2, 3]; return n + from;"),
            Value::Number(5.0)
        );
        assert_eq!(
            eval_in_fn("const [a, , c] = [10, 20, 30]; return a + c;"),
            Value::Number(40.0)
        );
    }

    #[test]
    fn multiple_declarators_in_one_statement_all_bind() {
        // Real Nova usage, right at the top of the file: `const DESIGN_W =
        // 1440, DESIGN_H = 900;`. Before this, the declaration parser only
        // read one `name (= value)?` and left a dangling `,` for the next
        // statement to choke on — it would see the comma, try to parse it
        // as the start of a new expression statement, and refuse with a
        // confusing "unexpected `,`; expected an expression" that pointed
        // nowhere near the real cause.
        assert_eq!(
            eval_in_fn("const a = 1, b = 2, c = a + b; return c;"),
            Value::Number(3.0)
        );
        // A declarator with no initializer, mixed with ones that have one —
        // `var`/`let` both allow this.
        assert_eq!(
            eval_in_fn("let x, y = 5; x = 10; return x + y;"),
            Value::Number(15.0)
        );
    }

    #[test]
    fn multiple_declarators_at_top_level_all_become_real_globals() {
        // Same root cause as `top_level_destructuring_creates_real_global_
        // bindings`: a multi-declarator statement desugars to the same
        // `Stmt::Sequence` destructuring already relies on, so it must be
        // visible to the top-level pass's global-store handling the exact
        // same way.
        let program = compile(
            "const DESIGN_W = 1440, DESIGN_H = 900; \
             function main() { record(DESIGN_W + DESIGN_H); } main();",
        )
        .expect("compiles");
        let mut host = RecordingHost::new();
        Vm::default()
            .run_with_host(&program, &mut host)
            .expect("runs");
        assert_eq!(host.calls, vec![2340.0]);
    }

    #[test]
    fn object_destructuring_binds_shorthand_renamed_and_defaulted_properties() {
        // Shorthand: `const { visTabs, hidTabs } = ...`.
        assert_eq!(
            eval_in_fn("const {a, b} = {a: 1, b: 2}; return a + b;"),
            Value::Number(3.0)
        );
        // Renamed: `function PageHeader({ icon: Ic, ... })`.
        assert_eq!(
            eval_in_fn("const {icon: Ic} = {icon: 5}; return Ic;"),
            Value::Number(5.0)
        );
        // Defaulted, property absent: `function FavImg({ d, size = 12 })`.
        assert_eq!(
            eval_in_fn("const {size = 12} = {}; return size;"),
            Value::Number(12.0)
        );
        // Defaulted, property genuinely `undefined`: same fallback.
        assert_eq!(
            eval_in_fn("const {size = 12} = {size: undefined}; return size;"),
            Value::Number(12.0)
        );
        // Defaulted, but the property IS present and falsy: `zoom = 1`
        // destructuring an explicit `zoom: 0` must keep 0, not silently
        // treat "falsy" as "absent" the way a naive `x || default` would.
        assert_eq!(
            eval_in_fn("const {zoom = 1} = {zoom: 0}; return zoom;"),
            Value::Number(0.0)
        );
    }

    #[test]
    fn destructured_function_parameters_bind_shorthand_renamed_and_defaulted_props() {
        // `function Fav({ f, size })` shape. `describe` and `main` are
        // top-level siblings, not nested — a *nested* function declaration
        // is a separate, pre-existing, unrelated restriction this test must
        // not trip over.
        let program = compile(
            "function describe({ label, size }) { return label + size; } \
             function main() { return describe({ label: \"x\", size: 3 }); } \
             main();",
        )
        .expect("compiles");
        assert_eq!(
            Vm::default()
                .call(&program, "main", Vec::new(), &mut NoHost::default())
                .expect("runs"),
            Value::String("x3".to_string())
        );
        // Renamed and defaulted together: `function PageHeader({ icon: Ic,
        // maxW = 880 })`.
        let program = compile(
            "function header({ icon: Ic, maxW = 880 }) { return Ic + maxW; } \
             function main() { return header({ icon: 1 }); } \
             main();",
        )
        .expect("compiles");
        assert_eq!(
            Vm::default()
                .call(&program, "main", Vec::new(), &mut NoHost::default())
                .expect("runs"),
            Value::Number(881.0)
        );
    }

    #[test]
    fn destructured_arrow_parameters_work() {
        // `({ t, c }) => ...`, a real Nova shape.
        assert_eq!(
            eval_in_fn("let f = ({t, c}) => t + c; return f({t: 1, c: 2});"),
            Value::Number(3.0)
        );
    }

    #[test]
    fn destructuring_refuses_rest_and_nested_patterns_rather_than_mishandling_them() {
        assert!(matches!(
            compile("const [a, ...rest] = [1, 2, 3];"),
            Err(JsError::Unsupported { .. })
        ));
        assert!(matches!(
            compile("const {a, ...rest} = {a: 1};"),
            Err(JsError::Unsupported { .. })
        ));
        assert!(matches!(
            compile("const [[a, b]] = [[1, 2]];"),
            Err(JsError::Unsupported { .. })
        ));
        assert!(matches!(
            compile("const {a: {b}} = {a: {b: 1}};"),
            Err(JsError::Unsupported { .. })
        ));
    }

    #[test]
    fn a_parenthesised_expression_is_not_mistaken_for_an_arrow() {
        // `(a + b)` is an ordinary grouped expression, not a parameter list.
        assert_eq!(
            eval_in_fn("let a = 2; let b = 3; return (a + b) * 2;"),
            Value::Number(10.0)
        );
    }

    #[test]
    fn an_arrow_captures_a_const_and_refuses_a_mutable() {
        // Arrows use the same capture path: a const is captured, a let refused.
        let program = compile(
            "function main() { const step = 3; let f = x => x + step; return f(39); } main();",
        )
        .expect("compiles");
        assert_eq!(
            Vm::default()
                .call(&program, "main", Vec::new(), &mut NoHost::default())
                .expect("runs"),
            Value::Number(42.0)
        );
        assert!(matches!(
            compile("function main() { let n = 5; let f = () => n; return f(); } main();"),
            Err(JsError::Unsupported { .. })
        ));
    }

    #[test]
    fn a_named_function_expression_compiles_with_the_name_unbound() {
        // Was refused outright; now compiles — see
        // `a_named_function_expression_compiles_with_the_name_dropped` for
        // the real Nova usage that motivated this and the value-level
        // regression test, and `a_named_function_expression_that_actually_
        // self_references_still_refuses` for what still refuses.
        assert!(compile("let f = function named() { return 1; };").is_ok());
    }

    #[test]
    fn array_holes_and_spread_are_refused() {
        assert!(matches!(
            compile("let a = [1, , 3];"),
            Err(JsError::Unsupported { .. })
        ));
        assert!(matches!(
            compile("let a = [...b];"),
            Err(JsError::Unsupported { .. })
        ));
    }

    #[test]
    fn for_loops_desugar_correctly() {
        // Classic counted loop: sum 0..5.
        assert_eq!(
            eval_in_fn(
                "let sum = 0; \
                 for (let i = 0; i < 5; i = i + 1) { sum = sum + i; } \
                 return sum;"
            ),
            Value::Number(10.0)
        );
        // The loop variable is scoped to the for statement's block, not
        // visible after — a second `let i` outside must not collide.
        assert_eq!(
            eval_in_fn(
                "for (let i = 0; i < 3; i = i + 1) {} \
                 let i = 99; \
                 return i;"
            ),
            Value::Number(99.0)
        );
        // Omitted clauses: no init, no update, and a body that exits itself.
        assert_eq!(
            eval_in_fn(
                "let n = 0; \
                 for (;;) { n = n + 1; if (n >= 3) { return n; } }"
            ),
            Value::Number(3.0)
        );
    }

    #[test]
    fn increment_and_decrement_operators() {
        // Prefix returns the new value.
        assert_eq!(eval_in_fn("let x = 5; return ++x;"), Value::Number(6.0));
        assert_eq!(eval_in_fn("let x = 5; return --x;"), Value::Number(4.0));
        // Postfix returns the old value but still mutates.
        assert_eq!(
            eval_in_fn("let x = 5; let old = x++; return old;"),
            Value::Number(5.0)
        );
        assert_eq!(eval_in_fn("let x = 5; x++; return x;"), Value::Number(6.0));
        assert_eq!(eval_in_fn("let x = 5; x--; return x;"), Value::Number(4.0));
        // Incrementing a const is refused, like any other assignment to one.
        assert!(matches!(
            compile("function main() { const x = 1; x++; } main();"),
            Err(JsError::AssignmentToConstant { .. })
        ));
    }

    #[test]
    fn compound_assignment_operators() {
        assert_eq!(
            eval_in_fn("let x = 5; x += 3; return x;"),
            Value::Number(8.0)
        );
        assert_eq!(
            eval_in_fn("let x = 5; x -= 3; return x;"),
            Value::Number(2.0)
        );
        assert_eq!(
            eval_in_fn("let x = 5; x *= 3; return x;"),
            Value::Number(15.0)
        );
        assert_eq!(
            eval_in_fn("let x = 6; x /= 3; return x;"),
            Value::Number(2.0)
        );
        // Compound assignment to an object property.
        assert_eq!(
            eval_in_fn("let o = { n: 5 }; o.n += 10; return o.n;"),
            Value::Number(15.0)
        );
        // Compound assignment to a const is refused.
        assert!(matches!(
            compile("function main() { const x = 1; x += 1; } main();"),
            Err(JsError::AssignmentToConstant { .. })
        ));
        // A computed key on the left of a compound assignment.
        assert_eq!(
            eval_in_fn("let a = [1, 2, 3]; a[1] += 10; return a[1];"),
            Value::Number(12.0)
        );
    }

    /// Records each call made through `record(n)`, so a test can observe
    /// what ran and in what order without a real embedder.
    #[derive(Debug, Default)]
    struct RecordingHost {
        bindings: Bindings,
        calls: Vec<f64>,
    }

    impl RecordingHost {
        fn new() -> Self {
            let mut bindings = Bindings::new();
            bindings.register("Test", "record", 1);
            Self {
                bindings,
                calls: Vec::new(),
            }
        }
    }

    impl Host for RecordingHost {
        fn bindings(&self) -> &Bindings {
            &self.bindings
        }

        fn invoke(
            &mut self,
            _interface: &str,
            name: &str,
            arguments: &[Value],
        ) -> Result<Value, String> {
            assert_eq!(name, "record");
            self.calls.push(to_number(&arguments[0]));
            Ok(Value::Undefined)
        }
    }

    #[test]
    fn queue_microtask_runs_after_the_synchronous_script_and_in_order() {
        let program = compile(
            "function main() { \
                record(1); \
                queueMicrotask(function() { record(3); }); \
                record(2); \
                queueMicrotask(function() { record(4); }); \
             } main();",
        )
        .expect("compiles");
        let mut host = RecordingHost::new();
        Vm::default()
            .call(&program, "main", Vec::new(), &mut host)
            .expect("runs");
        assert_eq!(
            host.calls,
            vec![1.0, 2.0, 3.0, 4.0],
            "synchronous calls run first, in order; queued ones follow, in queue order"
        );
    }

    #[test]
    fn a_microtask_that_queues_another_is_drained_in_the_same_flush() {
        let program = compile(
            "function main() { \
                queueMicrotask(function() { \
                    record(1); \
                    queueMicrotask(function() { record(2); }); \
                }); \
             } main();",
        )
        .expect("compiles");
        let mut host = RecordingHost::new();
        Vm::default()
            .call(&program, "main", Vec::new(), &mut host)
            .expect("runs");
        assert_eq!(
            host.calls,
            vec![1.0, 2.0],
            "a microtask queued during draining still runs before control returns"
        );
    }

    #[test]
    fn queue_microtask_accepts_a_closure_and_carries_its_captured_const() {
        let program = compile(
            "function main() { \
                const tag = 42; \
                queueMicrotask(function() { record(tag); }); \
             } main();",
        )
        .expect("compiles");
        let mut host = RecordingHost::new();
        Vm::default()
            .call(&program, "main", Vec::new(), &mut host)
            .expect("runs");
        assert_eq!(host.calls, vec![42.0]);
    }

    #[test]
    fn queue_microtask_rejects_a_non_function_and_the_wrong_arity() {
        let program = compile("function main() { queueMicrotask(5); } main();").expect("compiles");
        assert!(matches!(
            Vm::default().call(&program, "main", Vec::new(), &mut NoHost::default()),
            Err(JsError::TypeError { .. })
        ));
        assert!(matches!(
            compile("queueMicrotask();"),
            Err(JsError::OperationArity { .. })
        ));
        assert!(matches!(
            compile("queueMicrotask(a, b);"),
            Err(JsError::OperationArity { .. })
        ));
    }

    #[test]
    fn a_queued_closure_survives_collection_before_it_runs() {
        // The closure sits in the microtask queue, referenced from nowhere
        // else, while allocation-heavy work runs before the queue drains. If
        // the collector does not treat the queue as a root set, this
        // reclaims the closure and the later call reads freed data instead
        // of refusing cleanly or running correctly — it must do the latter.
        let program = compile(
            "function main() { \
                const tag = 7; \
                queueMicrotask(function() { record(tag); }); \
                let i = 0; \
                while (i < 200) { \
                    let churn = { a: i, b: i }; \
                    i = i + 1; \
                } \
             } main();",
        )
        .expect("compiles");
        let mut host = RecordingHost::new();
        Vm::default()
            .call(&program, "main", Vec::new(), &mut host)
            .expect("runs");
        assert_eq!(
            host.calls,
            vec![7.0],
            "the queued closure ran correctly after the churn"
        );
    }

    #[test]
    fn compound_assignment_evaluates_the_object_and_key_exactly_once() {
        // `getTarget().n += 10` must call `getTarget()` once, not twice. A
        // const-captured array records a call each time getTarget runs — its
        // reference is stable (const), but what it points to is ordinarily
        // mutable, which is what makes it a call counter here rather than a
        // capture-mutation test.
        let program = compile(
            "function main() { \
                const counter = []; \
                let getTarget = function() { \
                    counter[counter.length] = 1; \
                    let o = {}; \
                    o.n = 5; \
                    return o; \
                }; \
                getTarget().n += 10; \
                return counter.length; \
             } main();",
        )
        .expect("compiles");
        assert_eq!(
            Vm::default()
                .call(&program, "main", Vec::new(), &mut NoHost::default())
                .expect("runs"),
            Value::Number(1.0),
            "getTarget() must run exactly once"
        );

        // A computed key must likewise be evaluated once.
        let program = compile(
            "function main() { \
                const counter = []; \
                let nextKey = function() { \
                    counter[counter.length] = 1; \
                    return 0; \
                }; \
                let a = [5]; \
                a[nextKey()] += 10; \
                return counter.length; \
             } main();",
        )
        .expect("compiles");
        assert_eq!(
            Vm::default()
                .call(&program, "main", Vec::new(), &mut NoHost::default())
                .expect("runs"),
            Value::Number(1.0),
            "nextKey() must run exactly once"
        );
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
    fn string_length_and_built_in_methods_work() {
        assert_eq!(expr("\"hello\".length"), Value::Number(5.0));
        assert_eq!(
            expr("\"example.com/page\".indexOf(\"/\")"),
            Value::Number(11.0)
        );
        assert_eq!(expr("\"example.com\".indexOf(\"/\")"), Value::Number(-1.0));
        assert_eq!(expr("\"hello\".includes(\"ell\")"), Value::Boolean(true));
        assert_eq!(expr("\"hello\".startsWith(\"he\")"), Value::Boolean(true));
        assert_eq!(
            expr("\"Hello\".toLowerCase()"),
            Value::String("hello".to_string())
        );
        assert_eq!(
            expr("\"Hello\".toUpperCase()"),
            Value::String("HELLO".to_string())
        );
        assert_eq!(expr("\"  hi  \".trim()"), Value::String("hi".to_string()));
        assert_eq!(
            expr("\"a-b-c\".replace(\"-\", \"+\")"),
            Value::String("a+b-c".to_string()),
            "replace touches only the first occurrence, like real String.prototype.replace"
        );
        // The real Nova shape: `i === -1 ? url : url.slice(0, i)`.
        assert_eq!(
            expr("\"example.com/page\".slice(0, 11)"),
            Value::String("example.com".to_string())
        );
        assert_eq!(
            expr("\"example.com/page\".slice(11)"),
            Value::String("/page".to_string())
        );
        // Negative indices count from the end.
        assert_eq!(
            expr("\"hello\".slice(-3)"),
            Value::String("llo".to_string())
        );
    }

    #[test]
    fn string_split_returns_a_real_array() {
        assert_eq!(
            eval_in_fn("let parts = \"a,b,c\".split(\",\"); return parts.length;"),
            Value::Number(3.0)
        );
        assert_eq!(
            eval_in_fn("let parts = \"a,b,c\".split(\",\"); return parts[1];"),
            Value::String("b".to_string())
        );
        assert_eq!(
            eval_in_fn("let parts = \"ab\".split(\"\"); return parts.length;"),
            Value::Number(2.0),
            "an empty separator splits into individual characters"
        );
    }

    #[test]
    fn regex_literal_test_matches_and_respects_anchors_and_flags() {
        assert_eq!(
            expr("/^(input|textarea)$/i.test(\"INPUT\")"),
            Value::Boolean(true)
        );
        assert_eq!(
            expr("/^(input|textarea)$/i.test(\"my input\")"),
            Value::Boolean(false)
        );
        assert_eq!(expr("/[a-z]+/.test(\"42\")"), Value::Boolean(false));
        assert_eq!(expr("/[a-z]+/.test(\"ok\")"), Value::Boolean(true));
    }

    #[test]
    fn regex_literal_stored_and_called_later_still_works() {
        // The real Nova shape: a regex literal held in an array, called
        // through a later-bound variable's `.test()` — see the `RULES`
        // array use case in the `turing-nova-source-real-scope` project
        // memory's regex audit.
        assert_eq!(
            eval_in_fn(
                "let rules = [/^http:/, /^https:/]; let re = rules[1]; \
                 return re.test(\"https://example.com\");"
            ),
            Value::Boolean(true)
        );
    }

    #[test]
    fn new_regexp_compiles_a_runtime_pattern() {
        assert_eq!(
            eval_in_fn("let re = new RegExp(\"^ab+c$\", \"i\"); return re.test(\"ABBC\");"),
            Value::Boolean(true)
        );
        assert_eq!(
            eval_in_fn("let re = new RegExp(\"^ab+c$\"); return re.test(\"xyz\");"),
            Value::Boolean(false)
        );
    }

    #[test]
    fn new_with_any_other_constructor_still_refuses() {
        let result = compile("function main() { return new Thing(); } main();");
        assert!(matches!(result, Err(JsError::Unsupported { .. })));
    }

    #[test]
    fn division_still_lexes_correctly_after_identifiers_and_closing_parens() {
        // The real Nova shape this disambiguation must not break:
        // `w / DESIGN_W, (h - 56) / DESIGN_H` — division following both a
        // bare identifier and a closing paren, never a regex start.
        assert_eq!(
            eval_in_fn(
                "let w = 10; let designW = 5; let h = 106; let designH = 25; \
                 return (w / designW) + ((h - 56) / designH);"
            ),
            Value::Number(4.0)
        );
    }

    #[test]
    fn replace_with_a_regex_is_a_typed_refusal_not_a_panic() {
        // The literal itself compiles fine — the refusal is specifically
        // for calling `.replace()` with it, deferred stateful/interactive-
        // only behavior (see `mod regex`'s module doc comment).
        let program =
            compile("function main() { return \"a.b.c\".replace(/\\./g, \"-\"); } main();")
                .expect("the regex literal itself compiles");
        let error = Vm::default()
            .call(&program, "main", Vec::new(), &mut NoHost::default())
            .expect_err("regex .replace() is refused, not silently wrong");
        assert!(matches!(error, JsError::Unsupported { .. }));
    }

    #[test]
    fn array_built_in_methods_without_a_callback_work() {
        assert_eq!(
            eval_in_fn("let a = [1, 2]; a.push(3); return a.length;"),
            Value::Number(3.0)
        );
        assert_eq!(
            eval_in_fn("let a = [1, 2]; a.push(3); return a[2];"),
            Value::Number(3.0)
        );
        assert_eq!(
            eval_in_fn("return [1, 2, 3].join(\"-\");"),
            Value::String("1-2-3".to_string())
        );
        assert_eq!(expr("[1, 2, 3].indexOf(2)"), Value::Number(1.0));
        assert_eq!(expr("[1, 2, 3].indexOf(9)"), Value::Number(-1.0));
        assert_eq!(expr("[1, 2, 3].includes(2)"), Value::Boolean(true));
        assert_eq!(expr("[1, 2, 3].includes(9)"), Value::Boolean(false));
        assert_eq!(
            eval_in_fn("let s = [1, 2, 3, 4].slice(1, 3); return s.length + s[0];"),
            Value::Number(4.0),
            "slice(1, 3) of [1,2,3,4] is [2, 3]: length 2 plus element 0 (2) is 4"
        );
    }

    #[test]
    fn array_built_in_methods_with_a_callback_work() {
        assert_eq!(
            eval_in_fn("let m = [1, 2, 3].map(x => x * 2); return m[0] + m[1] + m[2];"),
            Value::Number(12.0)
        );
        assert_eq!(
            eval_in_fn("let f = [1, 2, 3, 4].filter(x => x > 2); return f.length + f[0];"),
            Value::Number(5.0),
            "filter(x > 2) of [1,2,3,4] is [3, 4]: length 2 plus element 0 (3) is 5"
        );
        // forEach has no return value of its own; observe it ran via a
        // captured side effect instead.
        let program = compile("function main() { [1, 2, 3].forEach(x => record(x)); } main();")
            .expect("compiles");
        let mut host = RecordingHost::new();
        Vm::default()
            .run_with_host(&program, &mut host)
            .expect("runs");
        assert_eq!(host.calls, vec![1.0, 2.0, 3.0]);
        assert_eq!(
            eval_in_fn("return [1, 2, 3].find(x => x > 1);"),
            Value::Number(2.0)
        );
        assert_eq!(
            eval_in_fn("return [1, 2, 3].find(x => x > 9);"),
            Value::Undefined
        );
        assert_eq!(
            eval_in_fn("return [1, 2, 3].findIndex(x => x > 1);"),
            Value::Number(1.0)
        );
        assert_eq!(
            eval_in_fn("return [1, 2, 3].some(x => x > 2);"),
            Value::Boolean(true)
        );
        assert_eq!(
            eval_in_fn("return [1, 2, 3].some(x => x > 9);"),
            Value::Boolean(false)
        );
        assert_eq!(
            eval_in_fn("return [1, 2, 3].reduce((acc, x) => acc + x, 0);"),
            Value::Number(6.0)
        );
        assert_eq!(
            eval_in_fn("return [1, 2, 3].reduce((acc, x) => acc + x);"),
            Value::Number(6.0),
            "reduce with no initial value seeds the accumulator from element 0"
        );
    }

    #[test]
    fn a_callback_may_declare_fewer_parameters_than_the_method_conventionally_passes() {
        // `map` conventionally passes (item, index), but a callback that only
        // declares `item` must still work — real JS ignores unused trailing
        // arguments rather than refusing the call.
        assert_eq!(
            eval_in_fn("let m = [10, 20].map(x => x + 1); return m[0] + m[1];"),
            Value::Number(32.0)
        );
    }

    #[test]
    fn an_own_property_named_like_a_built_in_method_shadows_it() {
        // Real own-property-shadows-prototype precedence: a stored callback
        // prop that happens to be named `filter` must still be called as
        // itself, not treated as Array.prototype.filter (this receiver is
        // an ordinary object, not even an array, so the built-in path could
        // never legitimately apply — the point is that resolution checks
        // the own property first, unconditionally).
        assert_eq!(
            eval_in_fn(
                "let o = { filter: function(x) { return x + 100; } }; \
                 return o.filter(1);"
            ),
            Value::Number(101.0)
        );
    }

    #[test]
    fn calling_an_unrecognised_method_is_a_typed_refusal_not_a_panic() {
        let program = compile("function main() { \"hi\".bogus(); } main();").expect("compiles");
        assert!(matches!(
            Vm::default().call(&program, "main", Vec::new(), &mut NoHost::default()),
            Err(JsError::TypeError { .. })
        ));
        let program = compile("function main() { [1, 2].bogus(); } main();").expect("compiles");
        assert!(matches!(
            Vm::default().call(&program, "main", Vec::new(), &mut NoHost::default()),
            Err(JsError::TypeError { .. })
        ));
        // A receiver type with no built-in methods at all (unlike String/
        // Array) still refuses rather than silently returning `undefined`.
        let program = compile("function main() { (5).bogus(); } main();").expect("compiles");
        assert!(matches!(
            Vm::default().call(&program, "main", Vec::new(), &mut NoHost::default()),
            Err(JsError::TypeError { .. })
        ));
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
        // Computed keys change what an initialiser means rather than only
        // how it is written, so a partial implementation would silently
        // drop properties the author wrote. (Shorthand properties and
        // method shorthand — `{ a }`, `{ m() {...} }` — used to be refused
        // here too; both are now implemented, see
        // `object_literal_shorthand_property_binds_key_to_the_same_name_
        // variable` and `object_literal_method_shorthand_desugars_to_a_
        // callable_property`.)
        let source = "let o = { ['computed']: 1 };";
        assert!(
            matches!(compile(source), Err(JsError::Unsupported { .. })),
            "expected a refusal for {source}"
        );
    }

    #[test]
    fn object_spread_copies_own_properties() {
        assert_eq!(
            eval_in_fn("let a = { x: 1, y: 2 }; let b = { ...a }; return b.x + b.y;"),
            Value::Number(3.0)
        );
        // A later explicit property, spread, or repeated key always wins
        // over an earlier one — spreading is just an ordinary sequence of
        // property writes in source order, not a special merge rule.
        assert_eq!(
            eval_in_fn("let b = { x: 1, ...{ x: 2 } }; return b.x;"),
            Value::Number(2.0),
            "a spread after an explicit property overrides it"
        );
        assert_eq!(
            eval_in_fn("let a = { x: 1 }; let b = { ...a, x: 3 }; return b.x;"),
            Value::Number(3.0),
            "an explicit property after a spread overrides it"
        );
        assert_eq!(
            eval_in_fn(
                "let a = { x: 1, y: 2 }; let b = { ...a, y: 9, z: 3 }; \
                 return b.x + b.y + b.z;"
            ),
            Value::Number(13.0),
            "spread properties merge alongside explicit ones, not instead of them"
        );
    }

    #[test]
    fn object_spread_of_null_or_undefined_spreads_nothing() {
        assert_eq!(
            eval_in_fn("let b = { ...null, ...undefined, x: 1 }; return b.x;"),
            Value::Number(1.0)
        );
    }

    #[test]
    fn object_spread_of_a_non_object_is_a_typed_refusal_not_a_panic() {
        let program = compile("function main() { return { ...5 }; } main();").expect("compiles");
        assert!(matches!(
            Vm::default().call(&program, "main", Vec::new(), &mut NoHost::default()),
            Err(JsError::TypeError { .. })
        ));
    }

    #[test]
    fn object_spread_matches_the_real_nova_style_merge_pattern() {
        // The exact shape Nova's real `Fav` component uses (turing-nova-
        // design-source.jsx:1707-1711): a style object built by spreading a
        // fallback-or-override object and then adding two more properties.
        assert_eq!(
            eval_in_fn(
                "let ff = { style: { background: \"red\" } }; \
                 let s = { ...(ff.style || { background: \"var(--c4)\" }), width: 15, height: 15 }; \
                 return s.background;"
            ),
            Value::String("red".to_string())
        );
        assert_eq!(
            eval_in_fn(
                "let ff = {}; \
                 let s = { ...(ff.style || { background: \"var(--c4)\" }), width: 15, height: 15 }; \
                 return s.background;"
            ),
            Value::String("var(--c4)".to_string()),
            "no style on ff falls back to the default background"
        );
    }

    #[test]
    fn object_literal_shorthand_property_binds_key_to_the_same_name_variable() {
        // `{ name }` is shorthand for `{ name: name }` — valid only for an
        // identifier-origin key.
        assert_eq!(
            eval_in_fn("let name = \"Nova\"; let obj = { name }; return obj.name;"),
            Value::String("Nova".to_string())
        );
        assert_eq!(
            eval_in_fn("let a = 1; let b = 2; let obj = { a, b }; return obj.a + obj.b;"),
            Value::Number(3.0)
        );
    }

    #[test]
    fn object_literal_method_shorthand_desugars_to_a_callable_property() {
        // `{ greet() { ... } }` desugars to `{ greet: function() { ... } }`
        // — an ordinary `Expr::Lambda` value, called the same way any other
        // function-valued property already is.
        assert_eq!(
            eval_in_fn("let obj = { greet() { return \"hi\"; } }; return obj.greet();"),
            Value::String("hi".to_string())
        );
        assert_eq!(
            eval_in_fn("let obj = { add(a, b) { return a + b; } }; return obj.add(2, 3);"),
            Value::Number(5.0)
        );
    }

    #[test]
    fn a_named_function_expression_compiles_with_the_name_dropped() {
        // Real Nova usage: `memo(function Toggle(...) {...})`, React's
        // devtools-name idiom for an inline component. Confirmed by grep
        // across every real `memo(function Name(...) {...})` in the file
        // (8 occurrences) that the name is never referenced inside its own
        // body — the name is consumed and dropped, not bound as a
        // capturable local.
        assert_eq!(
            eval_in_fn("let f = function greet() { return \"hi\"; }; return f();"),
            Value::String("hi".to_string())
        );
        assert_eq!(
            eval_in_fn("let add = function sum(a, b) { return a + b; }; return add(2, 3);"),
            Value::Number(5.0)
        );
    }

    #[test]
    fn a_named_function_expression_that_actually_self_references_still_refuses() {
        // The discriminating case: dropping the name rather than binding it
        // must not silently swallow a genuine self-reference. `fib` is not
        // bound as a local anywhere, so a call to it inside its own body
        // resolves the same way any other unresolved name would — as a
        // host operation, checked at the call site since the compiler does
        // not hold the host's table (see `Expr::Call`'s own doc comment on
        // this resolution order) — and since no host binds `fib`, running
        // it refuses with a typed `UnboundOperation`, not a wrong answer.
        // Proves the drop is honest: it would not silently compute the
        // wrong value for a script that actually meant self-recursion.
        let program = compile(
            "function main() { let f = function fib(n) { return fib(n); }; return f(1); } main();",
        )
        .expect("compiles");
        let error = Vm::default()
            .call(&program, "main", Vec::new(), &mut NoHost::default())
            .expect_err("refused");
        assert!(matches!(error, JsError::UnboundOperation { .. }));
    }

    #[test]
    fn delete_removes_a_property_by_dot_or_bracket_access() {
        // Real Nova usage: `delete rowEl.dataset.dragged`, `delete g[gid]`,
        // `delete scrollMem.current[id]` — always a member expression,
        // dot or bracket, ending in an object/array whose property goes
        // away. `delete` itself evaluates to `true`.
        assert_eq!(
            eval_in_fn(
                "let o = { a: 1, b: 2 }; \
                 let removed = delete o.a; \
                 return removed && o.a === undefined && o.b === 2;"
            ),
            Value::Boolean(true)
        );
        assert_eq!(
            eval_in_fn(
                "let o = {}; o[\"k\"] = 5; \
                 let removed = delete o[\"k\"]; \
                 return removed && o.k === undefined;"
            ),
            Value::Boolean(true)
        );
        // Deleting a key that was never present still returns `true` —
        // real JS `delete` semantics for a configurable (here: every)
        // property, present or not.
        assert_eq!(
            eval_in_fn("let o = {}; return delete o.nope;"),
            Value::Boolean(true)
        );
    }

    #[test]
    fn delete_as_a_bare_statement_is_not_refused_before_it_parses() {
        // The exact real Nova shape: `delete g[gid];` and `delete scrollMem.
        // current[id];` are always bare statements, not an assignment or
        // return value's operand. `delete` is intentionally absent from
        // `REFUSED_KEYWORDS` (see that constant's own doc comment) because
        // `Parser::parse_statement_inner` runs a blanket keyword check
        // against that table *before any expression parsing at all* — with
        // `delete` present there, every real call site would have refused
        // before `parse_unary_inner`'s own, more specific handling ever ran,
        // even though the exact same source works fine as an assignment's
        // right-hand side (see `delete_removes_a_property_by_dot_or_
        // bracket_access`, which never triggered this).
        assert_eq!(
            eval_in_fn("let o = { a: 1 }; delete o.a; return o.a === undefined;"),
            Value::Boolean(true)
        );
    }

    #[test]
    fn delete_on_an_array_element_removes_it_without_shrinking_length() {
        // Arrays share the same object heap representation as plain
        // objects (see `Value::Array`'s own doc comment) — `delete arr[i]`
        // removes that index's own property the same way, and — matching
        // real JS — does not shift later elements down or shrink `length`;
        // the slot just reads back `undefined`.
        assert_eq!(
            eval_in_fn(
                "let a = [1, 2, 3]; delete a[1]; \
                 return a[0] + (a[1] === undefined ? 0 : a[1]) + a[2] + a.length;"
            ),
            Value::Number(1.0 + 0.0 + 3.0 + 3.0)
        );
    }

    #[test]
    fn delete_of_anything_but_a_member_expression_still_refuses() {
        // Real usage never targets a bare variable — refused rather than
        // silently doing nothing (deleting a local binding is not
        // meaningful in this engine's model, unlike a real property).
        assert!(matches!(
            compile("let x = 1; delete x;"),
            Err(JsError::Unsupported { .. })
        ));
    }

    #[test]
    fn object_literal_shorthand_with_a_non_identifier_key_still_refuses() {
        // `{ "a" }`/`{ 1 }` are not legal JS shorthand — only an
        // identifier-origin key may omit its value.
        assert!(matches!(
            compile("function main() { let obj = { \"a\" }; } main();"),
            Err(JsError::Unsupported { .. })
        ));
    }

    #[test]
    fn object_literal_getter_setter_and_generator_methods_still_refuse() {
        // None of these appear in real Nova usage; each must refuse by
        // name rather than being silently mis-parsed as some other shape.
        // `get`/`set` are ordinary identifiers to this engine, so `get x()`
        // reaches the new method-shorthand branch's fallback refusal
        // (`Unsupported`); `async` is already a reserved keyword refused
        // earlier, at the property-name token match itself (`UnexpectedToken`
        // — still a typed refusal, just from an earlier, more general check).
        assert!(matches!(
            compile("function main() { let obj = { get x() { return 1; } }; } main();"),
            Err(JsError::Unsupported { .. })
        ));
        assert!(matches!(
            compile("function main() { let obj = { async x() {} }; } main();"),
            Err(JsError::UnexpectedToken { .. })
        ));
    }

    #[test]
    fn template_literals_interpolate_expressions() {
        assert_eq!(expr("`a${1 + 1}b`"), Value::String("a2b".to_string()));
        assert_eq!(
            expr("`no interpolation`"),
            Value::String("no interpolation".to_string())
        );
        assert_eq!(expr("``"), Value::String(String::new()));
        assert_eq!(
            eval_in_fn("let x = 1; let y = 2; return `${x}:${y}`;"),
            Value::String("1:2".to_string()),
            "back-to-back interpolations with no literal text between them"
        );
        assert_eq!(expr("`${1}${2}${3}`"), Value::String("123".to_string()));
    }

    #[test]
    fn template_literal_interpolation_can_be_an_arbitrary_expression() {
        // Not just a bare variable — the interpolation is parsed as a real
        // expression, method calls and ternaries included.
        assert_eq!(
            eval_in_fn("let s = \"hello\"; return `${s.slice(0, 2)}!`;"),
            Value::String("he!".to_string())
        );
        assert_eq!(
            expr("`${1 > 0 ? \"yes\" : \"no\"}`"),
            Value::String("yes".to_string())
        );
    }

    #[test]
    fn template_literal_matches_the_real_nova_translate_pattern() {
        // Nova line 1815 (`turing-nova-design-source.jsx`): a CSS
        // transform built from a single numeric interpolation, the most
        // common template-literal shape in the real file.
        let source = "function main() { let s = styleFor(42); return s.transform; } \
             function styleFor(y) { return { transform: `translateY(${y}px)` }; } \
             main();";
        assert_eq!(
            run_main_source(source),
            Value::String("translateY(42px)".to_string())
        );
    }

    #[test]
    fn template_literal_preserves_non_ascii_text_around_an_interpolation() {
        // Nova line 2402 uses curly quotes around an interpolation — a
        // direct check that the byte-level scan (ASCII delimiters only)
        // does not corrupt surrounding multi-byte UTF-8 text.
        assert_eq!(
            eval_in_fn(
                "let seedText = \"why is the sky blue\"; \
                 return `\u{201c}${seedText.slice(0, 3)}\u{201d} \u{2014} what does this mean?`;"
            ),
            Value::String("\u{201c}why\u{201d} \u{2014} what does this mean?".to_string())
        );
    }

    #[test]
    fn nested_template_literals_are_refused_not_partially_evaluated() {
        assert!(matches!(
            compile("let x = `a${`b`}c`;"),
            Err(JsError::Unsupported { .. })
        ));
    }

    #[test]
    fn an_unterminated_template_literal_is_a_typed_refusal_not_a_panic() {
        assert!(matches!(
            compile("let x = `unterminated;"),
            Err(JsError::UnexpectedToken { .. })
        ));
        assert!(
            matches!(
                compile("let x = `unterminated ${1 + 1;"),
                Err(JsError::UnexpectedToken { .. })
            ),
            "an unterminated interpolation refuses the same way"
        );
    }

    #[test]
    fn import_default_and_named_bindings_resolve_through_an_existing_global() {
        // The import itself never creates a binding for a non-aliased
        // name — it compiles to nothing — so this only proves `useState`
        // (standing in for a prelude-provided global) was already
        // reachable the whole time, exactly the way a real prelude
        // function like `memo` already is.
        let source = "import React, { useState } from \"react\"; \
             function main() { return useState(4); } \
             function useState(x) { return x + 1; } main();";
        assert_eq!(run_main_source(source), Value::Number(5.0));
    }

    #[test]
    fn import_with_an_alias_creates_a_new_binding() {
        // `run_main_source` calls `main` directly, bypassing the top-level
        // script body — but the alias binding this test exercises is a
        // top-level `const`, whose initializer only runs as part of that
        // top-level body (a `function` declaration needs no such run, since
        // it compiles to a compile-time-constant reference instead — that
        // is why the *other* import test above can use `run_main_source`
        // safely and this one cannot). Using the full `run_with_host` path
        // instead runs the import's initializer for real, the way any
        // actual script execution already does.
        let program = compile(
            "import { History as HistoryIcon } from \"lucide-react\"; \
             function History() { return 7; } \
             function main() { record(HistoryIcon()); } main();",
        )
        .expect("compiles");
        let mut host = RecordingHost::new();
        Vm::default()
            .run_with_host(&program, &mut host)
            .expect("runs");
        assert_eq!(host.calls, vec![7.0]);
    }

    #[test]
    fn import_from_an_unlisted_module_is_refused() {
        assert!(matches!(
            compile("import { x } from \"some-random-npm-package\";"),
            Err(JsError::Unsupported { .. })
        ));
    }

    #[test]
    fn import_namespace_and_side_effect_forms_are_refused() {
        assert!(matches!(
            compile("import * as React from \"react\";"),
            Err(JsError::Unsupported { .. })
        ));
        assert!(matches!(
            compile("import \"react\";"),
            Err(JsError::Unsupported { .. })
        ));
    }

    #[test]
    fn export_default_function_compiles_as_an_ordinary_top_level_function() {
        let source = "function main() { return Widget(); } \
             export default function Widget() { return 9; } main();";
        assert_eq!(run_main_source(source), Value::Number(9.0));
    }

    #[test]
    fn other_export_forms_are_refused() {
        assert!(matches!(
            compile("export const x = 1;"),
            Err(JsError::Unsupported { .. })
        ));
        assert!(matches!(
            compile("export default 5;"),
            Err(JsError::Unsupported { .. })
        ));
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
    fn array_methods_root_remaining_elements_and_accumulator_across_a_collection() {
        // `map` reads the source array into a Rust-side `Vec<Value>` and
        // builds a second one (`mapped`) as it goes — neither lives on
        // stack/locals, so they are invisible to `collect_now` unless
        // explicitly rooted. `build(n)` alone already pushes occupied heap
        // slots past the collection trigger, so from the very first
        // callback call onward almost every further allocation (each
        // mapped `{v:...}` object, then the result array itself) runs with
        // `occupied_slots() >= COLLECT_AFTER_ALLOCATIONS` and triggers a
        // real collection — no separate junk-allocation loop needed. A
        // rooting gap around either vector would free a not-yet-visited
        // source element or an already-produced result mid-loop, and the
        // later read-back would see a stale/reused slot instead of the
        // real value.
        let n = COLLECT_AFTER_ALLOCATIONS + 8;
        let source = format!(
            "function main() {{ \
                 let source = build({n}); \
                 let mapped = source.map(churn); \
                 let total = 0; let i = 0; \
                 while (i < mapped.length) {{ total = total + mapped[i].v; i = i + 1; }} \
                 return total; \
             }} \
             function build(n) {{ \
                 let a = []; let i = 0; \
                 while (i < n) {{ a.push({{ v: i }}); i = i + 1; }} \
                 return a; \
             }} \
             function churn(x) {{ \
                 return {{ v: x.v + 1 }}; \
             }} \
             main();"
        );
        // source is [{{v:0}}..{{v:n-1}}], mapped is [{{v:1}}..{{v:n}}]: the
        // sum telescopes to 1+2+...+n.
        let expected: f64 = (1..=n).map(|v| v as f64).sum();
        assert_eq!(run_main_source(&source), Value::Number(expected));
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

    /// A hand-built, deliberately malformed program: no compiler emits this,
    /// but nothing here proves the interpreter can never receive a program
    /// it did not compile itself, and `panic = "abort"` in the release
    /// profile means any panic reachable from bytecode takes the whole
    /// embedding process down with it, not just this one call.
    fn malformed_program(op: Op) -> Program {
        Program {
            functions: vec![Function {
                name: "main".to_owned(),
                arity: 0,
                min_arity: 0,
                locals: 0,
                code: vec![op, Op::Return],
            }],
        }
    }

    #[test]
    fn new_array_with_no_operands_on_the_stack_does_not_panic() {
        // `Op::NewArray(5)` with nothing pushed first: `stack.len() - 5`
        // would underflow. Before the fix this panicked (in the dev profile,
        // where overflow-checks = true) or wrapped to a huge index and
        // panicked inside `split_off` (release) — either way, a crash rather
        // than the refusal this codebase's own rule requires.
        let program = malformed_program(Op::NewArray(5));
        let result = Vm::default().run_with_host(&program, &mut NoHost::default());
        assert!(
            result.is_ok(),
            "a malformed NewArray operand count must not panic, got {result:?}"
        );
    }

    #[test]
    fn make_closure_with_no_operands_on_the_stack_does_not_panic() {
        // Same hazard, `Op::MakeClosure`'s own operand count: claiming 3
        // captured upvalues with an empty stack. `index: 0` names the
        // top-level function itself, which is not meaningful as a captured
        // closure body, but the point of this test is that building one
        // does not crash the process — not that the result is useful.
        let program = malformed_program(Op::MakeClosure {
            index: 0,
            upvalues: 3,
        });
        let result = Vm::default().run_with_host(&program, &mut NoHost::default());
        assert!(
            result.is_ok(),
            "a malformed MakeClosure operand count must not panic, got {result:?}"
        );
    }

    // -- JSX ----------------------------------------------------------------
    //
    // JSX desugars entirely at parse time (see the module-level doc comment
    // on JSX), so most of these assert on `compile`'s `Result` rather than
    // on a run: a lowercase tag name compiles without the name being
    // declared (it became a string), an uppercase one does not (it became a
    // variable reference — the calling-convention claim these tests exist to
    // pin down), and every construct that does compile calls the
    // well-known, deliberately unbound `__jsxCreateElement`, which running
    // confirms fails as `JsError::UnboundOperation` — neither a panic nor a
    // silent no-op, exactly like calling any other undeclared name.

    #[test]
    fn jsx_self_closing_tag_calls_the_unbound_create_element() {
        let program = compile("function main() { return <div />; } main();").expect("compiles");
        let error = Vm::default()
            .call(&program, "main", Vec::new(), &mut NoHost::default())
            .expect_err("__jsxCreateElement is not bound");
        assert_eq!(
            error,
            JsError::UnboundOperation {
                name: "__jsxCreateElement".to_string()
            }
        );
    }

    #[test]
    fn jsx_lowercase_tag_name_is_a_string_not_a_declared_name() {
        // A lowercase-leading tag is a host/intrinsic element and passes as
        // a string, so nothing named `div` needs to exist for this to
        // compile — the clearest proof the tag did not become a variable
        // reference.
        assert!(compile("function main() { return <div />; } main();").is_ok());
    }

    #[test]
    fn jsx_uppercase_tag_name_is_a_variable_reference() {
        // An uppercase-leading tag is a component reference and passes as
        // the identifier itself, so an undeclared one fails to compile as
        // an ordinary undefined variable — not as an unbound operation, and
        // not silently as the string `"Header"`.
        let error = compile("function main() { return <Header />; } main();")
            .expect_err("Header is not declared");
        assert_eq!(
            error,
            JsError::UndefinedVariable {
                name: "Header".to_string()
            }
        );

        // Declaring it resolves the reference; the only remaining failure
        // is the __jsxCreateElement call itself, at run time.
        let program = compile("function main() { let Header = 0; return <Header />; } main();")
            .expect("compiles once Header is declared");
        let error = Vm::default()
            .call(&program, "main", Vec::new(), &mut NoHost::default())
            .expect_err("__jsxCreateElement is still not bound");
        assert_eq!(
            error,
            JsError::UnboundOperation {
                name: "__jsxCreateElement".to_string()
            }
        );
    }

    #[test]
    fn jsx_attributes_accept_strings_and_expression_braces() {
        let program = compile(
            "function main() { let handler = 1; \
             return <div className=\"card\" onClick={handler} />; } main();",
        )
        .expect("compiles");
        let error = Vm::default()
            .call(&program, "main", Vec::new(), &mut NoHost::default())
            .expect_err("__jsxCreateElement is not bound");
        assert_eq!(
            error,
            JsError::UnboundOperation {
                name: "__jsxCreateElement".to_string()
            }
        );
    }

    #[test]
    fn jsx_attribute_expression_brace_accepts_an_arrow_function() {
        // The brace content is parsed with the ordinary expression grammar,
        // so an event-handler arrow works without any JSX-specific case for
        // it. `count` is `const`: an arrow only captures a `const` binding
        // (see the module docs on closures), so this is the one this test
        // can exercise without also tripping that unrelated refusal.
        assert!(
            compile(
                "function main() { const count = 0; \
             return <button onClick={() => count} />; } main();"
            )
            .is_ok()
        );
    }

    #[test]
    fn jsx_text_children_are_kept() {
        let program =
            compile("function main() { return <div>hello</div>; } main();").expect("compiles");
        let error = Vm::default()
            .call(&program, "main", Vec::new(), &mut NoHost::default())
            .expect_err("__jsxCreateElement is not bound");
        assert_eq!(
            error,
            JsError::UnboundOperation {
                name: "__jsxCreateElement".to_string()
            }
        );
    }

    #[test]
    fn jsx_text_may_contain_non_ascii_characters_unquoted() {
        // Real Nova text: curly quotes, a ⌘ glyph, and (in its own fixture
        // data) full Japanese titles and emoji, all written directly as
        // JSX text with no surrounding quotes at all. The *eager* lexer
        // that runs before JSX's own raw-byte scan takes over must not
        // choke on any of that — it previously errored on the very first
        // multi-byte character reached outside a string/comment.
        assert!(compile("function main() { return <span>⌘T \u{201c}quoted\u{201d} 日本語 🚀</span>; } main();").is_ok());
    }

    #[test]
    fn jsx_text_may_contain_a_bare_ampersand_or_an_html_entity() {
        // Real Nova text: a literal HTML entity ("Wade's Plumbing &amp;
        // Septic LLC") and, elsewhere in the file, bare `&` used as the
        // word "and" ("Cookies & site data") — neither is JavaScript, and
        // this engine has no bitwise-AND operator for a bare `&` to mean
        // anyway. The eager lexer must tolerate it here the same way it
        // already tolerates non-ASCII bytes in JSX text.
        assert!(
            compile("function main() { return <div>Total &amp; &nbsp; Cookies & site data</div>; } main();")
                .is_ok()
        );
    }

    #[test]
    fn an_unsupported_operator_inside_a_jsx_expression_or_interpolation_still_refuses() {
        // The gap a real bitwise `&` (Nova's `rgba` helper: `(n >> 16) &
        // 255`) would fall into if eager-lex tolerance were applied
        // unconditionally instead of only to the whole-file pass: `&`
        // inside a JSX `{expr}` or a template-literal interpolation is
        // real code, re-lexed strictly by `parse_embedded_expression`/
        // `parse_expression_from_source` — it must refuse, not silently
        // vanish from the token stream.
        let jsx_expr =
            compile("function main() { let a = 1; let b = 2; return <div>{a & b}</div>; } main();");
        assert!(
            matches!(
                jsx_expr,
                Err(JsError::UnexpectedCharacter { character: '&', .. })
            ),
            "a bitwise `&` inside a JSX expression must refuse, got {jsx_expr:?}"
        );
        let interpolation =
            compile("function main() { let a = 1; let b = 2; return `${a & b}`; } main();");
        assert!(
            matches!(
                interpolation,
                Err(JsError::UnexpectedCharacter { character: '&', .. })
            ),
            "a bitwise `&` inside a template interpolation must refuse, got {interpolation:?}"
        );
    }

    #[test]
    fn jsx_expression_children_are_parsed_as_expressions() {
        let program =
            compile("function main() { let value = 1; return <div>{value}</div>; } main();")
                .expect("compiles");
        let error = Vm::default()
            .call(&program, "main", Vec::new(), &mut NoHost::default())
            .expect_err("__jsxCreateElement is not bound");
        assert_eq!(
            error,
            JsError::UnboundOperation {
                name: "__jsxCreateElement".to_string()
            }
        );
    }

    #[test]
    fn jsx_nested_tags_and_mixed_children_compile() {
        // Text, a nested element, and an expression child together, in one
        // parent — the mixed-content case, and deep enough to exercise
        // `jsx_children`'s recursion into `jsx_element` for the nested tag.
        let program = compile(
            "function main() { let name = \"world\"; \
             return <div>Hello, <span>{name}</span>!</div>; } main();",
        )
        .expect("compiles");
        let error = Vm::default()
            .call(&program, "main", Vec::new(), &mut NoHost::default())
            .expect_err("__jsxCreateElement is not bound");
        assert_eq!(
            error,
            JsError::UnboundOperation {
                name: "__jsxCreateElement".to_string()
            }
        );
    }

    #[test]
    fn jsx_fragment_uses_a_fragment_variable_reference() {
        // A stretch-goal construct: `<>...</>` desugars like a component
        // reference naming `Fragment`, so it is refused as undefined until
        // something named `Fragment` is in scope — the same proof pattern
        // as the uppercase-tag test above.
        let error = compile("function main() { return <><div /></>; } main();")
            .expect_err("Fragment is not declared");
        assert_eq!(
            error,
            JsError::UndefinedVariable {
                name: "Fragment".to_string()
            }
        );

        let program =
            compile("function main() { let Fragment = 0; return <><div /><span /></>; } main();")
                .expect("compiles once Fragment is declared");
        let error = Vm::default()
            .call(&program, "main", Vec::new(), &mut NoHost::default())
            .expect_err("__jsxCreateElement is still not bound");
        assert_eq!(
            error,
            JsError::UnboundOperation {
                name: "__jsxCreateElement".to_string()
            }
        );
    }

    #[test]
    fn jsx_spread_attributes_are_refused_at_compile_time_not_a_panic() {
        let result = compile("function main() { return <div {...props} />; } main();");
        assert!(
            matches!(result, Err(JsError::Unsupported { .. })),
            "spread attributes must be a named refusal, got {result:?}"
        );
    }

    #[test]
    fn jsx_boolean_shorthand_attribute_is_refused() {
        let result = compile("function main() { return <input disabled />; } main();");
        assert!(matches!(result, Err(JsError::Unsupported { .. })));
    }

    #[test]
    fn jsx_namespaced_tag_name_is_refused() {
        let result = compile("function main() { return <Foo.Bar />; } main();");
        assert!(matches!(result, Err(JsError::Unsupported { .. })));
    }

    #[test]
    fn less_than_comparison_still_parses_as_a_comparison_not_jsx() {
        // The one ambiguity JSX introduces at the token level: `<` in
        // expression position. `jsx_ahead` only fires when an identifier or
        // `>` immediately follows, and a plain comparison's `<` is examined
        // by `parse_comparison` after its left operand already consumed the
        // first identifier — so this must still evaluate as `a < b`, not
        // fail trying to parse `b` as a tag name.
        assert_eq!(
            run_main("let a = 1; let b = 2; return a < b;"),
            Value::Boolean(true)
        );
        assert_eq!(expr("1 < 2"), Value::Boolean(true));
    }

    #[test]
    fn jsx_whitespace_only_between_siblings_produces_no_stray_text_child() {
        // Ordinarily-indented multi-line JSX: the whitespace runs before and
        // after `<span />` must not become extra entries in the children
        // array. Every `__jsxCreateElement` call now has a fixed arity of
        // three (tag, props, children array) regardless of child count, so
        // the count that matters is the *children array's own* length, not
        // the call's argument count — checked via the `Op::NewArray` that
        // builds it.
        let program = compile("function main() { return <div>\n  <span />\n</div>; } main();")
            .expect("compiles");
        let outer_call_position = program.functions[1]
            .code
            .iter()
            .rposition(|op| matches!(op, Op::HostCall(name, _) if name == "__jsxCreateElement"))
            .expect("an outer __jsxCreateElement call");
        let Some(Op::NewArray(count)) = program.functions[1].code[..outer_call_position]
            .iter()
            .rfind(|op| matches!(op, Op::NewArray(_)))
        else {
            panic!("expected a NewArray building the outer call's children argument");
        };
        // Exactly one child (the nested `<span />`'s own
        // `__jsxCreateElement` result) — not more, which is what stray
        // whitespace-only text children would add.
        assert_eq!(*count, 1);
    }

    #[test]
    fn jsx_deeply_nested_tags_refuse_rather_than_overflow_the_stack() {
        // `jsx_element` is wrapped in `enter`/`leave` like every other
        // recursive production, so pathological nesting is a typed refusal,
        // not a crash. 2000 levels is far past `MAX_NESTING_DEPTH` and would
        // overflow the native stack if this recursion were unbounded.
        let mut source = "function main() { return ".to_string();
        for _ in 0..2000 {
            source.push_str("<a>");
        }
        for _ in 0..2000 {
            source.push_str("</a>");
        }
        source.push_str("; } main();");
        assert!(matches!(
            compile(&source),
            Err(JsError::NestingTooDeep { .. })
        ));
    }

    #[test]
    fn jsx_text_may_contain_a_raw_apostrophe_unquoted() {
        // Real Nova text writes English contractions/possessives directly
        // and unquoted in JSX ("...only what's on screen exists...",
        // "browser's own CSS engine", "Don't"). The eager whole-file lex
        // used to read a bare `'` as opening a real string-literal token
        // and scan forward to the next `'` (or end of input) looking for a
        // close, silently desynchronising everything JSX's own raw-byte
        // re-scan tries to resume from afterward — confirmed on the real
        // file: one apostrophe near byte 323116 swallowed ~25KB of real
        // code/JSX this way before `resume_at`'s mismatch check turned that
        // into at least a named (if confusingly-located) refusal.
        //
        // Fixed at the root: a genuine JS string literal can never contain
        // a raw newline, so the scan in `lex` now bails the moment it
        // crosses one without finding a closing quote — the same
        // "unrecognized byte in a to-be-discarded eager pass" tolerance
        // already applied to non-ASCII bytes and a bare `&` (see `lex`'s
        // `tolerate_unknown` doc comment), just reached via a different
        // signal. Verified against the real file: simulating this exact
        // scan found zero genuine single/double-quoted string literals
        // that span a newline, so the rule has no false positives there.
        assert!(compile("function main() { return <div>Don't</div>; } main();").is_ok());
        assert!(
            compile(
                "function main() { return <p>...only what's on screen exists...</p>; } main();"
            )
            .is_ok()
        );
    }

    #[test]
    fn an_unterminated_string_inside_a_jsx_expression_or_interpolation_still_refuses() {
        // Mirrors the bitwise-`&` refusal test above for the same reason:
        // only the eager whole-file pass may treat a stray quote as "not
        // really a string open" and back out (see `lex`'s
        // `tolerate_unknown` doc comment) — the two strict re-lex paths
        // (a JSX `{expr}` body, a template-literal interpolation) must
        // still refuse a genuinely unterminated string literal by name,
        // not silently drop the quote as if it were inert JSX text.
        let jsx_expr =
            compile("function main() { return <div>{'unterminated\nstring'}</div>; } main();");
        assert!(
            matches!(
                jsx_expr,
                Err(JsError::UnexpectedCharacter {
                    character: '\'',
                    ..
                })
            ),
            "an unterminated string inside a JSX expression must refuse, got {jsx_expr:?}"
        );
    }

    #[test]
    fn jsx_wrapped_in_parens_with_surrounding_whitespace_still_compiles() {
        // Regression test: real, ordinarily-formatted multi-line JSX —
        // `return (\n  <div>...</div>\n);`, the common style for wrapping a
        // JSX expression across several lines — used to be refused by
        // `resume_at` as a desync, purely because of the insignificant
        // whitespace between the JSX's closing tag and the following `)`.
        // No earlier JSX test happened to leave whitespace in that specific
        // gap, so nothing had caught it until real, hand-written JSX (not a
        // synthetic single-line test string) exercised it.
        let cases = [
            "function main() { return (\n<div className=\"x\">hi</div>\n); } main();",
            "function main() { return ( <div className=\"x\">hi</div> ); } main();",
            "function main() { return (<div className=\"x\">hi</div>\n); } main();",
        ];
        for source in cases {
            assert!(
                compile(source).is_ok(),
                "whitespace around a parenthesised JSX expression must not be a desync: {source:?}"
            );
        }
    }
}
