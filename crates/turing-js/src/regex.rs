// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at https://mozilla.org/MPL/2.0/.

//! A regular-expression engine scoped to what this project's real usage
//! needs (see the `turing-nova-source-real-scope` project memory for the
//! audit this was built from: 25 uses in the literal Nova design source,
//! all short patterns — anchors, character classes with `\d`/`\s`/`\w`
//! shorthands, alternation, greedy quantifiers, and the `i`/`g` flags),
//! not general ECMAScript regex compliance.
//!
//! # Why Thompson/Pike, not backtracking
//!
//! A naive backtracking matcher is the usual choice for a small regex
//! engine, but it is also the classic source of catastrophic exponential
//! blowup on inputs like `(a+)+b` against a non-matching string — exactly
//! the kind of hostile-input risk this interpreter's other budgets (step
//! limit, byte limit, nesting depth) all exist to rule out. This engine
//! instead compiles patterns to a small NFA (Thompson's construction) and
//! simulates it breadth-first over the input (Pike's VM, the technique
//! behind RE2/Rust's `regex` crate) — matching time is bounded by
//! `pattern_size * text_size` with no exponential case, at the cost of not
//! supporting backreferences (which real Nova usage never needs).
//!
//! # Deliberately refused, not silently approximated
//!
//! Backreferences, lookaround (`(?=`, `(?!`, `(?<=`, `(?<!`), named groups,
//! non-greedy quantifiers (`*?`, `+?`, `??`), and flags other than `g`/`i`
//! all return a [`RegexError`] from [`compile_pattern`] rather than
//! matching partially or wrong.

/// A compiled pattern: its source text (for `.toString()`/display), its
/// flags, and the NFA program the matcher simulates.
///
/// `pub`, not `pub(crate)`: it appears as a field of `Value::Regex`, which
/// is itself `pub` for embedders outside this crate — the type needs a
/// real external path to be nameable there, which this struct gets via
/// the `pub use regex::CompiledRegex` re-export at the crate root, while
/// `mod regex` itself, and every other item in this module, stays
/// crate-private. Its fields stay `pub(crate)`: an embedder can hold and
/// pass this value around (through `Value`) without being able to read or
/// construct one directly.
#[derive(Clone, Debug, PartialEq)]
pub struct CompiledRegex {
    pub(crate) source: String,
    pub(crate) flags: String,
    pub(crate) ignore_case: bool,
    pub(crate) global: bool,
    program: Vec<Inst>,
}

/// A pattern this engine cannot compile: unimplemented syntax, or a
/// malformed pattern. Carries a message rather than a taxonomy of causes —
/// the caller (`turing-js`'s compiler/VM) wraps it in [`super::JsError`],
/// which is where a caller-facing category belongs.
#[derive(Clone, Debug, PartialEq)]
pub(crate) struct RegexError {
    pub(crate) message: String,
}

impl std::fmt::Display for RegexError {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(formatter, "{}", self.message)
    }
}

fn unsupported(message: impl Into<String>) -> RegexError {
    RegexError {
        message: message.into(),
    }
}

// -- instructions ----------------------------------------------------------

#[derive(Clone, Debug, PartialEq)]
enum Inst {
    Char(char),
    /// `.` — anything but `\n` (this engine has no multiline/dotall flag,
    /// so `\n` exclusion is the one behavior real usage ever observes).
    Any,
    Class(ClassSet),
    /// `^` — true only at the very start of the text (no `m` flag, so this
    /// is a whole-string anchor, not a per-line one).
    Start,
    /// `$` — true only at the very end of the text, for the same reason.
    End,
    Jmp(usize),
    /// Try `.0` before `.1` — the priority order that gives greedy
    /// quantifiers and first-alternative-preferred alternation their real
    /// JS semantics under Pike's VM.
    Split(usize, usize),
    Match,
}

#[derive(Clone, Debug, PartialEq)]
struct ClassSet {
    negated: bool,
    /// Inclusive ranges. Pre-folded to lowercase at compile time when the
    /// pattern is case-insensitive — see `compile_pattern`'s call to
    /// `fold_case`.
    ranges: Vec<(char, char)>,
}

impl ClassSet {
    fn matches(&self, ch: char) -> bool {
        let hit = self.ranges.iter().any(|&(lo, hi)| ch >= lo && ch <= hi);
        hit != self.negated
    }
}

/// Instruction-count ceiling a compiled pattern may not exceed.
///
/// Real Nova patterns compile to a few dozen instructions at most. This
/// exists for `new RegExp(runtimeString)`, whose pattern is not fixed at
/// compile time — without a cap, a script could hand a huge `{0,N}`
/// quantifier count (or a long run of them) to force a very large
/// allocation. Refusing past this point matches the step/byte budgets
/// this interpreter already enforces elsewhere: a bound on work per
/// construct, not a guess at what "normal" looks like.
///
/// Checked from *inside* `compile_node`/`compile_repeat`, not only once
/// after the whole program is built: `{m,n}` bounded by
/// [`MAX_QUANTIFIER_BOUND`] still expands by emitting `m` full copies of
/// its sub-pattern, and nested quantifiers compound that — three levels
/// of `{1000}` alone would build on the order of a billion instructions
/// before a single after-the-fact check ever ran. Checking at every
/// `compile_node` entry point instead means a pattern like
/// `(((a{1000}){1000}){1000})` bails within one nested unit of overshoot,
/// not after building the explosion.
const MAX_PROGRAM_SIZE: usize = 10_000;

/// A single `{m,n}` bound (and the equivalent for `{m,}`) may not exceed
/// this. Otherwise a pattern like `a{0,999999999}` — one repeated atom —
/// could alone blow through `MAX_PROGRAM_SIZE` well before a size check on
/// the finished program would catch it, or simply take a long time to
/// build the instructions for.
const MAX_QUANTIFIER_BOUND: u32 = 1_000;

/// Recursive-descent nesting ceiling for the pattern parser (parenthesised
/// groups), mirroring [`super::MAX_NESTING_DEPTH`]'s reason for existing:
/// this parser recurses with the call stack, and an adversarial pattern
/// string — reachable at runtime through `new RegExp(runtimeString)`, not
/// just from source text — could otherwise force a stack overflow, which
/// aborts the process rather than producing a [`RegexError`].
const MAX_GROUP_DEPTH: usize = 64;

/// Compiles `pattern`/`flags` (the two halves of a `/pattern/flags` literal,
/// or the two arguments to `new RegExp`) into a matcher.
///
/// # Errors
///
/// Returns [`RegexError`] for a flag other than `g`/`i`, for syntax this
/// engine does not implement (backreferences, lookaround, named or
/// non-greedy groups, `{m,n}` past [`MAX_QUANTIFIER_BOUND`]), for a
/// malformed pattern, or for a pattern whose compiled program would exceed
/// [`MAX_PROGRAM_SIZE`].
pub(crate) fn compile_pattern(pattern: &str, flags: &str) -> Result<CompiledRegex, RegexError> {
    let mut global = false;
    let mut ignore_case = false;
    for flag in flags.chars() {
        match flag {
            'g' => global = true,
            'i' => ignore_case = true,
            other => {
                return Err(unsupported(format!(
                    "the regular-expression flag '{other}'; only 'g' and 'i' are implemented"
                )));
            }
        }
    }

    let mut parser = PatternParser {
        chars: pattern.chars().collect(),
        pos: 0,
        depth: 0,
    };
    let mut ast = parser.parse_alternation()?;
    if parser.pos != parser.chars.len() {
        return Err(unsupported(format!(
            "unexpected '{}' at position {} of the pattern",
            parser.chars[parser.pos], parser.pos
        )));
    }
    if ignore_case {
        ast = fold_case(ast);
    }

    let mut program = Vec::new();
    compile_node(&ast, &mut program)?;
    program.push(Inst::Match);
    check_budget(&program)?;

    Ok(CompiledRegex {
        source: pattern.to_string(),
        flags: flags.to_string(),
        ignore_case,
        global,
        program,
    })
}

/// Whether `regex` matches anywhere in `text` — `RegExp.prototype.test`.
///
/// Tries every start position against the (unanchored, unless the pattern
/// itself opens with `^`) pattern. This is `O(len(text)^2 * pattern_size)`
/// rather than the `O(len(text) * pattern_size)` a single unanchored Pike's-
/// VM pass achieves by injecting a fresh thread at every position within
/// one pass — deliberately the simpler of the two to keep this matcher
/// easy to verify, which is the right trade for the short UI strings real
/// usage matches against (menu labels, URLs, form values), not documents.
pub(crate) fn test(regex: &CompiledRegex, text: &str) -> bool {
    let chars: Vec<char> = if regex.ignore_case {
        text.chars().map(|ch| ch.to_ascii_lowercase()).collect()
    } else {
        text.chars().collect()
    };
    for start in 0..=chars.len() {
        if matches_from(&regex.program, &chars, start) {
            return true;
        }
    }
    false
}

/// Whether the program reaches `Inst::Match` by consuming a (possibly
/// empty) prefix of `text[start..]`, starting the walk at `start`.
fn matches_from(program: &[Inst], text: &[char], start: usize) -> bool {
    let mut current = Vec::new();
    let mut visited = vec![false; program.len()];
    add_thread(
        program,
        0,
        start == 0,
        start == text.len(),
        &mut current,
        &mut visited,
    );
    if current
        .iter()
        .any(|&program_counter| matches!(program[program_counter], Inst::Match))
    {
        return true;
    }

    let mut position = start;
    while position < text.len() && !current.is_empty() {
        let ch = text[position];
        let mut next = Vec::new();
        let mut visited = vec![false; program.len()];
        for &program_counter in &current {
            let advances = match &program[program_counter] {
                Inst::Char(expected) => ch == *expected,
                Inst::Any => ch != '\n',
                Inst::Class(set) => set.matches(ch),
                Inst::Match => false,
                Inst::Jmp(_) | Inst::Split(_, _) | Inst::Start | Inst::End => {
                    unreachable!("add_thread never leaves an epsilon instruction in `current`")
                }
            };
            if advances {
                add_thread(
                    program,
                    program_counter + 1,
                    position + 1 == 0,
                    position + 1 == text.len(),
                    &mut next,
                    &mut visited,
                );
            }
        }
        position += 1;
        current = next;
        if current
            .iter()
            .any(|&program_counter| matches!(program[program_counter], Inst::Match))
        {
            return true;
        }
    }
    false
}

/// Adds `program_counter` and everything reachable from it through
/// epsilon transitions (`Jmp`, `Split`, and a satisfied `Start`/`End`) to
/// `list`, so `list` only ever holds "real" instructions (`Char`, `Any`,
/// `Class`, `Match`) — the ones a simulation step can actually advance
/// past or stop at. `visited` prevents both infinite loops (a `Split`
/// whose branches rejoin) and duplicate entries.
fn add_thread(
    program: &[Inst],
    program_counter: usize,
    at_start: bool,
    at_end: bool,
    list: &mut Vec<usize>,
    visited: &mut [bool],
) {
    if visited[program_counter] {
        return;
    }
    visited[program_counter] = true;
    match &program[program_counter] {
        Inst::Jmp(target) => add_thread(program, *target, at_start, at_end, list, visited),
        Inst::Split(first, second) => {
            add_thread(program, *first, at_start, at_end, list, visited);
            add_thread(program, *second, at_start, at_end, list, visited);
        }
        Inst::Start => {
            if at_start {
                add_thread(
                    program,
                    program_counter + 1,
                    at_start,
                    at_end,
                    list,
                    visited,
                );
            }
        }
        Inst::End => {
            if at_end {
                add_thread(
                    program,
                    program_counter + 1,
                    at_start,
                    at_end,
                    list,
                    visited,
                );
            }
        }
        Inst::Char(_) | Inst::Any | Inst::Class(_) | Inst::Match => list.push(program_counter),
    }
}

// -- AST and Thompson construction ------------------------------------------

#[derive(Clone, Debug, PartialEq)]
enum Node {
    Char(char),
    Any,
    Class(ClassSet),
    Start,
    End,
    Concat(Vec<Node>),
    Alt(Vec<Node>),
    Repeat {
        node: Box<Node>,
        min: u32,
        max: Option<u32>,
    },
}

fn fold_case(node: Node) -> Node {
    match node {
        Node::Char(ch) => Node::Char(ch.to_ascii_lowercase()),
        Node::Class(set) => Node::Class(ClassSet {
            negated: set.negated,
            ranges: set
                .ranges
                .into_iter()
                .map(|(lo, hi)| (lo.to_ascii_lowercase(), hi.to_ascii_lowercase()))
                .collect(),
        }),
        Node::Any | Node::Start | Node::End => node,
        Node::Concat(items) => Node::Concat(items.into_iter().map(fold_case).collect()),
        Node::Alt(items) => Node::Alt(items.into_iter().map(fold_case).collect()),
        Node::Repeat { node, min, max } => Node::Repeat {
            node: Box::new(fold_case(*node)),
            min,
            max,
        },
    }
}

/// Refuses once `program` has already grown past [`MAX_PROGRAM_SIZE`].
/// Called at the top of every [`compile_node`] entry (see that constant's
/// own doc comment for why "only check at the end" is not enough once
/// quantifiers can nest).
fn check_budget(program: &[Inst]) -> Result<(), RegexError> {
    if program.len() > MAX_PROGRAM_SIZE {
        return Err(unsupported(format!(
            "a pattern compiling to more than {MAX_PROGRAM_SIZE} instructions"
        )));
    }
    Ok(())
}

/// Appends `node`'s instructions to `program`. Each call leaves `program`
/// ready for the next sibling to append directly after — every emitted
/// jump target is either already known or backpatched before this returns.
fn compile_node(node: &Node, program: &mut Vec<Inst>) -> Result<(), RegexError> {
    check_budget(program)?;
    match node {
        Node::Char(ch) => program.push(Inst::Char(*ch)),
        Node::Any => program.push(Inst::Any),
        Node::Class(set) => program.push(Inst::Class(set.clone())),
        Node::Start => program.push(Inst::Start),
        Node::End => program.push(Inst::End),
        Node::Concat(items) => {
            for item in items {
                compile_node(item, program)?;
            }
        }
        Node::Alt(items) => compile_alt(items, program)?,
        Node::Repeat { node, min, max } => compile_repeat(node, *min, *max, program)?,
    }
    Ok(())
}

/// `a|b|c` compiles as a right-leaning chain of splits, each offering "try
/// this alternative" before "try the rest" — first-alternative-preferred,
/// matching JS.
fn compile_alt(items: &[Node], program: &mut Vec<Inst>) -> Result<(), RegexError> {
    let Some((first, rest)) = items.split_first() else {
        return Ok(());
    };
    if rest.is_empty() {
        return compile_node(first, program);
    }
    let split_at = program.len();
    program.push(Inst::Split(0, 0));
    let first_branch = program.len();
    compile_node(first, program)?;
    let jump_at = program.len();
    program.push(Inst::Jmp(0));
    let second_branch = program.len();
    compile_alt(rest, program)?;
    let end = program.len();
    program[split_at] = Inst::Split(first_branch, second_branch);
    program[jump_at] = Inst::Jmp(end);
    Ok(())
}

/// Expands `node{min,max}` (`max: None` for `{min,}`, including `*`/`+`) as
/// `min` mandatory copies followed either by a true loop (unbounded) or a
/// chain of optional copies that can each choose to stop (bounded) —
/// see the inline comments for why each shared "skip" target is correct.
///
/// Each copy compiles through `compile_node`, which re-checks the size
/// budget on entry — so `min`/`extra` being individually bounded by
/// [`MAX_QUANTIFIER_BOUND`] is not what keeps this from exploding when
/// quantifiers nest (`(a{1000}){1000}` would still build a million
/// instructions if only the *count* were bounded); the per-copy check is.
fn compile_repeat(
    node: &Node,
    min: u32,
    max: Option<u32>,
    program: &mut Vec<Inst>,
) -> Result<(), RegexError> {
    for _ in 0..min {
        compile_node(node, program)?;
    }
    match max {
        None => {
            let loop_start = program.len();
            let split_at = program.len();
            program.push(Inst::Split(0, 0));
            let body_start = program.len();
            compile_node(node, program)?;
            program.push(Inst::Jmp(loop_start));
            let after = program.len();
            program[split_at] = Inst::Split(body_start, after);
        }
        Some(max) => {
            let extra = max.saturating_sub(min);
            let mut splits = Vec::new();
            for _ in 0..extra {
                let split_at = program.len();
                program.push(Inst::Split(0, 0));
                splits.push(split_at);
                compile_node(node, program)?;
            }
            // Every optional copy's "don't take it" branch lands here.
            // Reaching split[k] at all already means copies 0..k were
            // taken (splits execute in sequence, one per compiled copy),
            // so "stop now" from any of them correctly means "exactly
            // that many copies, no more" — there is nothing between here
            // and `end` but the remaining optional copies themselves.
            let end = program.len();
            for split_at in splits {
                program[split_at] = Inst::Split(split_at + 1, end);
            }
        }
    }
    Ok(())
}

// -- pattern parser ----------------------------------------------------------

struct PatternParser {
    chars: Vec<char>,
    pos: usize,
    depth: usize,
}

enum ClassAtom {
    Single(char),
    Shorthand(Vec<(char, char)>),
}

const DIGIT: (char, char) = ('0', '9');
const WORD_RANGES: [(char, char); 4] = [('a', 'z'), ('A', 'Z'), ('0', '9'), ('_', '_')];
const SPACE_CHARS: [char; 6] = [' ', '\t', '\n', '\r', '\u{0B}', '\u{0C}'];

fn space_ranges() -> Vec<(char, char)> {
    SPACE_CHARS.iter().map(|&ch| (ch, ch)).collect()
}

impl PatternParser {
    fn peek(&self) -> Option<char> {
        self.chars.get(self.pos).copied()
    }

    fn advance_char(&mut self) -> Result<char, RegexError> {
        let ch = self
            .peek()
            .ok_or_else(|| unsupported("an unterminated regular expression"))?;
        self.pos += 1;
        Ok(ch)
    }

    fn parse_alternation(&mut self) -> Result<Node, RegexError> {
        let mut branches = vec![self.parse_concat()?];
        while self.peek() == Some('|') {
            self.pos += 1;
            branches.push(self.parse_concat()?);
        }
        Ok(if branches.len() == 1 {
            branches.into_iter().next().unwrap()
        } else {
            Node::Alt(branches)
        })
    }

    fn parse_concat(&mut self) -> Result<Node, RegexError> {
        let mut items = Vec::new();
        while !matches!(self.peek(), None | Some('|') | Some(')')) {
            items.push(self.parse_quantified()?);
        }
        Ok(match items.len() {
            1 => items.into_iter().next().unwrap(),
            _ => Node::Concat(items),
        })
    }

    fn parse_quantified(&mut self) -> Result<Node, RegexError> {
        let atom = self.parse_atom()?;
        match self.parse_quantifier()? {
            Some((min, max)) => Ok(Node::Repeat {
                node: Box::new(atom),
                min,
                max,
            }),
            None => Ok(atom),
        }
    }

    fn parse_quantifier(&mut self) -> Result<Option<(u32, Option<u32>)>, RegexError> {
        let bound = match self.peek() {
            Some('*') => {
                self.pos += 1;
                Some((0, None))
            }
            Some('+') => {
                self.pos += 1;
                Some((1, None))
            }
            Some('?') => {
                self.pos += 1;
                Some((0, Some(1)))
            }
            Some('{') => Some(self.parse_brace_quantifier()?),
            _ => None,
        };
        if bound.is_some() && self.peek() == Some('?') {
            self.pos += 1;
            return Err(unsupported(
                "a non-greedy quantifier ('*?', '+?', '??', or '{m,n}?')",
            ));
        }
        Ok(bound)
    }

    /// Parses `{m}`, `{m,}`, or `{m,n}`, `{` already peeked but not
    /// consumed. A `{` that turns out not to open a valid quantifier is a
    /// pattern this engine refuses rather than reinterprets as a literal
    /// brace — real usage never relies on that JS fallback behavior, and
    /// silently guessing which reading was meant is the wrong default for
    /// this codebase.
    fn parse_brace_quantifier(&mut self) -> Result<(u32, Option<u32>), RegexError> {
        let start = self.pos;
        self.pos += 1; // '{'
        let min = self.parse_digits();
        let (min, max) = match min {
            None => return Err(self.malformed_brace(start)),
            Some(min) => {
                if self.peek() == Some(',') {
                    self.pos += 1;
                    if self.peek() == Some('}') {
                        (min, None)
                    } else {
                        let Some(max) = self.parse_digits() else {
                            return Err(self.malformed_brace(start));
                        };
                        (min, Some(max))
                    }
                } else {
                    (min, Some(min))
                }
            }
        };
        if self.peek() != Some('}') {
            return Err(self.malformed_brace(start));
        }
        self.pos += 1;
        if min > MAX_QUANTIFIER_BOUND || max.is_some_and(|max| max > MAX_QUANTIFIER_BOUND) {
            return Err(unsupported(format!(
                "a repetition count above {MAX_QUANTIFIER_BOUND}"
            )));
        }
        if let Some(max) = max
            && max < min
        {
            return Err(unsupported("a `{m,n}` quantifier with n less than m"));
        }
        Ok((min, max))
    }

    fn malformed_brace(&self, start: usize) -> RegexError {
        unsupported(format!(
            "'{{' at position {start} not opening a valid `{{m}}`/`{{m,}}`/`{{m,n}}` quantifier"
        ))
    }

    fn parse_digits(&mut self) -> Option<u32> {
        let start = self.pos;
        while self.peek().is_some_and(|ch| ch.is_ascii_digit()) {
            self.pos += 1;
        }
        if self.pos == start {
            return None;
        }
        let text: String = self.chars[start..self.pos].iter().collect();
        text.parse().ok()
    }

    fn parse_atom(&mut self) -> Result<Node, RegexError> {
        match self.advance_char()? {
            '.' => Ok(Node::Any),
            '^' => Ok(Node::Start),
            '$' => Ok(Node::End),
            '[' => self.parse_class().map(Node::Class),
            '(' => self.parse_group(),
            '\\' => self.parse_escape(),
            ch @ ('*' | '+' | '?' | ')' | ']' | '{') => Err(unsupported(format!(
                "'{ch}' with nothing before it to repeat or close"
            ))),
            ch => Ok(Node::Char(ch)),
        }
    }

    fn parse_group(&mut self) -> Result<Node, RegexError> {
        self.depth += 1;
        if self.depth > MAX_GROUP_DEPTH {
            return Err(unsupported(format!(
                "groups nested past {MAX_GROUP_DEPTH} levels"
            )));
        }
        if self.peek() == Some('?') {
            // Only `(?:...)`, a plain non-capturing group, is implemented —
            // this engine never extracts captures, so it behaves exactly
            // like an ordinary group. `(?=`, `(?!`, `(?<`, and a bare `(?`
            // are all lookaround/named-group syntax this engine refuses.
            if self.chars.get(self.pos + 1) == Some(&':') {
                self.pos += 2;
            } else {
                return Err(unsupported(
                    "a lookaround or named-group construct ('(?=', '(?!', '(?<=', '(?<!', or '(?<name>')",
                ));
            }
        }
        let inner = self.parse_alternation()?;
        if self.peek() != Some(')') {
            return Err(unsupported("an unterminated group"));
        }
        self.pos += 1;
        self.depth -= 1;
        Ok(inner)
    }

    fn parse_escape(&mut self) -> Result<Node, RegexError> {
        match self.class_atom_after_backslash()? {
            ClassAtom::Shorthand(ranges) => Ok(Node::Class(ClassSet {
                negated: false,
                ranges,
            })),
            ClassAtom::Single(ch) => Ok(Node::Char(ch)),
        }
    }

    /// The shared body of an escape, whether it appears as a standalone
    /// atom (`\d` outside a class) or as one item inside `[...]`.
    fn class_atom_after_backslash(&mut self) -> Result<ClassAtom, RegexError> {
        let escaped = self.advance_char()?;
        match escaped {
            'd' => Ok(ClassAtom::Shorthand(vec![DIGIT])),
            's' => Ok(ClassAtom::Shorthand(space_ranges())),
            'w' => Ok(ClassAtom::Shorthand(WORD_RANGES.to_vec())),
            'D' | 'S' | 'W' => Err(unsupported(format!(
                "'\\{escaped}' (negated character-class shorthand)"
            ))),
            '1'..='9' => Err(unsupported("a backreference")),
            other => Ok(ClassAtom::Single(other)),
        }
    }

    fn parse_class(&mut self) -> Result<ClassSet, RegexError> {
        let negated = if self.peek() == Some('^') {
            self.pos += 1;
            true
        } else {
            false
        };
        let mut ranges = Vec::new();
        while self.peek() != Some(']') {
            if self.peek().is_none() {
                return Err(unsupported("an unterminated character class"));
            }
            let atom = self.parse_class_atom()?;
            match atom {
                ClassAtom::Shorthand(mut shorthand_ranges) => ranges.append(&mut shorthand_ranges),
                ClassAtom::Single(start) => {
                    if self.peek() == Some('-')
                        && self.chars.get(self.pos + 1).is_some_and(|&ch| ch != ']')
                    {
                        self.pos += 1; // '-'
                        match self.parse_class_atom()? {
                            ClassAtom::Single(end) => {
                                if end < start {
                                    return Err(unsupported(
                                        "a character-class range whose end is before its start",
                                    ));
                                }
                                ranges.push((start, end));
                            }
                            ClassAtom::Shorthand(_) => {
                                return Err(unsupported(
                                    "a character-class range ending in a shorthand like \\d",
                                ));
                            }
                        }
                    } else {
                        ranges.push((start, start));
                    }
                }
            }
        }
        self.pos += 1; // ']'
        Ok(ClassSet { negated, ranges })
    }

    fn parse_class_atom(&mut self) -> Result<ClassAtom, RegexError> {
        match self.advance_char()? {
            '\\' => self.class_atom_after_backslash(),
            ch => Ok(ClassAtom::Single(ch)),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn compiles(pattern: &str, flags: &str) -> CompiledRegex {
        compile_pattern(pattern, flags).expect("compiles")
    }

    #[test]
    fn literal_characters_match_a_substring_anywhere() {
        let regex = compiles("cat", "");
        assert!(test(&regex, "concatenate"));
        assert!(!test(&regex, "dog"));
    }

    #[test]
    fn anchors_restrict_the_match_to_the_whole_string() {
        let regex = compiles("^(input|textarea)$", "i");
        assert!(test(&regex, "input"));
        assert!(test(&regex, "TEXTAREA"));
        assert!(!test(&regex, "my input"));
        assert!(!test(&regex, "inputs"));
    }

    #[test]
    fn character_class_with_shorthand_and_negation() {
        let regex = compiles("[^A-Za-z0-9]", "");
        assert!(test(&regex, "a b"));
        assert!(!test(&regex, "abc123"));

        let digits = compiles("\\d+", "");
        assert!(test(&digits, "room 42"));
        assert!(!test(&digits, "no numbers here"));
    }

    #[test]
    fn quantifiers_are_greedy_and_bounded_forms_work() {
        assert!(test(&compiles("a{0,4}b", ""), "aaaab"));
        assert!(!test(&compiles("^a{0,4}$", ""), "aaaaa"));
        assert!(test(&compiles("colou?r", ""), "color"));
        assert!(test(&compiles("colou?r", ""), "colour"));
    }

    #[test]
    fn alternation_and_escaped_specials_inside_a_class() {
        // Nova's own search-highlighter escapes every regex metacharacter
        // this way before building a dynamic pattern from user input.
        let regex = compiles(r"[.*+?^${}()|[\]\\]", "g");
        for ch in ".*+?^${}()|[]\\".chars() {
            assert!(test(&regex, &ch.to_string()), "expected {ch:?} to match");
        }
        assert!(!test(&regex, "abc"));
    }

    #[test]
    fn non_capturing_group_behaves_like_a_plain_group() {
        let regex = compiles("(?:foo|bar)baz", "");
        assert!(test(&regex, "foobaz"));
        assert!(test(&regex, "barbaz"));
        assert!(!test(&regex, "bazbaz"));
    }

    #[test]
    fn unimplemented_syntax_is_refused_not_guessed() {
        assert!(compile_pattern("(a)\\1", "").is_err());
        assert!(compile_pattern("a(?=b)", "").is_err());
        assert!(compile_pattern("a*?", "").is_err());
        assert!(compile_pattern("[\\D]", "").is_err());
        assert!(compile_pattern("a", "m").is_err());
        assert!(compile_pattern("a{0,99999}", "").is_err());
    }

    #[test]
    fn a_pathological_repetition_pattern_matches_in_bounded_time() {
        // The classic backtracking blowup case. Pike's VM has no
        // exponential path, so this is expected to return quickly even
        // though the string never matches.
        let regex = compiles("(a+)+b", "");
        let hostile = "a".repeat(30);
        assert!(!test(&regex, &hostile));
    }

    #[test]
    fn nested_bounded_quantifiers_are_refused_quickly_not_expanded_first() {
        // Each `{1000}` alone is under MAX_QUANTIFIER_BOUND, but three
        // nested would multiply to roughly a billion instructions if the
        // size budget were only checked after the whole program was
        // built. This must return (refused) promptly, not hang or exhaust
        // memory building the explosion before the check ever runs.
        let result = compile_pattern("(((a{1000}){1000}){1000})", "");
        assert!(result.is_err());
    }
}
