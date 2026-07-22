# Turing as an Application Runtime

Status: architecture and milestone research; target architecture is defined in [Turing Platform Architecture](01-turing-platform-architecture.md)
Owner: product direction, architecture, engine, UI runtime, platform, security, performance, accessibility, and developer experience
Opened 2026-07-20; last reviewed 2026-07-22.

This book does not claim the runtime exists. It states the target, the honest
gap from today's engine, and the order the gap can be closed in.

The [Turing Platform Architecture](01-turing-platform-architecture.md) is the
canonical ownership and boundary contract. This book supplies capability-gap
and milestone detail; it cannot authorize implementation, select a toolkit,
or override security, source-strategy, or production controls.

## The target

Turing is not only a web browser. The owner's direction is that the Turing
engine become an **application runtime** — the way Electron lets a product
ship a React/Next.js/TanStack application as a desktop app, except that the
runtime and rendering path are Turing-owned, built from scratch, with no
Chromium, Blink, V8, external React runtime, or webview underneath.

Two concrete ambitions define the target:

1. **The system UI is the engine's own output.** The Nova design
   (`docs/ui-runtime/design-lab/turing-nova-design-source.jsx`) is React.
   The end state is that a Turing-owned JSX/component runtime can execute the
   captured source or a compatible compiled representation and the running
   result **is** the browser's chrome and, further out, the desktop system
   interface — not a hand-port of Nova into unrelated app-specific widgets. Today's
   `turing-chrome` crate is an honest interim: it renders Nova's design at
   reference fidelity from extracted tokens, which is what let the product
   look right before the engine could run the source. It is a stepping
   stone, explicitly not the destination.

2. **Real framework apps run on the engine.** A React application, a
   Next.js app, a TanStack app — the artifacts a working web developer
   produces — should load and run on Turing the way they load and run in a
   browser or an Electron shell.

## This direction changes the charter, and says so

Honesty first: the owner's direction here **extends and partly conflicts with
the accepted architecture**, and pretending otherwise would make this book
worthless.

- The product charter
  (`docs/blueprint-v1/01-charter-and-principles.md`) scopes Turing as "an
  independent desktop browser." An application runtime for third-party
  React/Next.js/TanStack apps is a larger product than that charter states.
- **ADR-0008** (`docs/blueprint-v1/17-architecture-decisions.md`) — accepted
  — keeps trusted browser chrome *independent from the web engine*, precisely
  so product reliability and security prompts do not ride on
  untrusted-content code paths. Rendering the system UI by *running its
  React on the engine* is the opposite of that decision.

Both are owner-held decisions, and @byronwade is the owner giving this
direction — so this book does not overrule the charter quietly; it records
that the direction **requires the charter and ADR-0008 to be revisited**, and
notes that ADR-0008 already left the narrow door: its "Revisit when" clause
admits the engine rendering *nonessential internal surfaces* once the engine
is mature enough and a security review approves the boundary, with critical
trusted controls still independent. The path this book lays out is meant to
reach that review with evidence, not to skip it. Until the charter and
ADR-0008 are formally amended, this is a **research direction**, not an
accepted product scope, and the two must not be conflated.

## Why this is the same engine, widened — not a second project

Electron is Chromium plus Node. Its power is that the app author writes
ordinary web code and a complete web engine renders it. Turing's bet is the
same shape with a different foundation: the app author writes ordinary web
code, and **Turing's from-scratch engine** renders it. Everything already
built serves this directly — the HTML tree, the CSS cascade, block and
inline layout, the display list, the reference and compositing painters, the
DOM with mutation epochs, the capability-scoped script bindings, the input
routing. An application runtime is not a pivot away from that work; it is
that work carried far enough to run a framework.

## What renders today

The engine already renders the **static HTML output** that every React
framework produces on the server. `benchmarks/corpus/framework-output/`
holds `nextjs-ssr-dashboard.html` — a dark-themed analytics dashboard with a
header, metric cards (borders, rounded corners, HSL theme colours), and a
centred call-to-action button — the exact shape of a Next.js server-rendered
page. It renders correctly through the normal pipeline with no special
casing.

This matters because it fixes the first rung: **server-rendered framework
output is already in scope and already works.** A Next.js app that ships
mostly static, server-rendered pages is closer to running on Turing than the
distance from here to a full client runtime suggests. The embedding book
already anticipates a headless **server-render mode**
(`docs/embedding/README.md`); rendering framework SSR output is that mode
pointed at real framework HTML.

The engine also already renders **the browser's own chrome** — the surface
this book's two ambitions are ultimately about — as ordinary HTML/CSS/JS
rather than hand-written Rust widgets:
`crates/turing-engine/examples/nova_chrome_demo.rs` and its companion
`.html` fixture describe a tab strip and an address/search pill using
colours and dimensions taken directly from `design/tokens.json` (the
machine-readable extraction of the hash-pinned Nova design source, not
approximated), load it through `Page::load` the same way any embedder would,
click a tab through `Page::dispatch_at`, and confirm the active tab's
background genuinely changed — through real `setAttribute` + relayout +
repaint, not a mock. This is **not** a claim that this replaces
`turing-chrome` as the browser's actual trusted chrome: that specific
substitution is exactly what `ADR-0008` and the charter conflict (above)
gate behind a security review, because an address bar rendered by the same
engine that renders untrusted page content is a real trust-boundary
question, not only an implementation detail. What it does show is that
`Page`'s existing, ordinary API is already capable of painting and driving
this UI from markup — the destination this book describes is a matter of
*deciding* to reach it, at APP-6/APP-7, not of proving the render path could
ever work at all.

The fixture also surfaced a real, previously undocumented layout gap while
being built: nothing in `turing-layout` currently threads an inline child's
own `margin` into how far the next sibling's pen position advances in
`layout_inline_children` — only content width and padding do. A `margin` on
a `display: inline` element therefore creates no gap before the next inline
sibling; only a genuine, non-whitespace-only text run between them does (a
purely-whitespace text node between two elements is discarded at
box-generation before layout ever sees it, so an empty `<span> </span>`
spacer does not work either). The fixture works around this with a literal
separator character; the gap itself is unfixed.

## The honest gap

Running a framework's *client* runtime — hydration, hooks, reconciliation,
event handlers — needs engine capability that does not exist yet. Named
plainly rather than glossed:

### JavaScript (`turing-js`)

The interpreter is a deliberately bounded subset: numbers, strings, booleans,
`null`/`undefined`, bindings, arithmetic and logic, control flow, `for`
loops, function declarations and expressions, arrow functions, calls,
recursion, first-class function values, closures over `const` bindings,
arrays, and objects with property access. What still refuses — by design,
at compile time or, for the array/object method surface, at the call itself
— are the remaining constructs a React runtime needs:

- **mutable capture**: a closure over an enclosing `let`/`var`, and
  multi-level capture, are refused rather than computed wrong (see APP-2
  below) — hooks closing over state that changes is the pattern this
  blocks;
- **`Array`/`Object` prototype methods** (`.push`, `.map`, `.forEach`,
  `.filter`, and the rest): array literals, indexing, `length`, and growth
  by index-write all work, but no method call on an array or object is
  bound yet — every JSX-adjacent `children.map(...)` pattern needs this;
- **`class`** (older React components, many libraries);
- **prototypes and `this` semantics**;
- **`try`/`catch`**, **`async`/`await`**, **generators**, **modules**,
  **regular expressions**.

This is the largest remaining gap, and it is the load-bearing one. It is
also already a planned program, not a new one:
`docs/blueprint-v1/06-javascript-runtime.md` and the `docs/javascript/` book
scope a full from-scratch ECMAScript engine — parser, bytecode interpreter,
generational GC, baseline and optimizing JIT, Web IDL bindings, WebAssembly,
and an event loop — explicitly "capable enough to eventually run React's
runtime as web content." What this book adds is a *reason to prioritise
that program toward framework support*, and a rung order for it. The
engine's governing principle is a strength for this goal, not a weakness: a
partially implemented language computes wrong values silently, so every
unimplemented construct is refused visibly — confirmed directly for the
array/object method gap: calling an unbound method returns a typed
`TypeError`, not a panic or a silently wrong value. The runtime grows one
honest construct at a time, and everything that runs stays trustworthy.

### DOM API surface

`turing-webidl` binds a real capability set now: `getAttribute`,
`setAttribute`, `removeAttribute`, `tagName`, `hasElement`, `textContent`,
`addEventListener`, `removeEventListener`, `documentBody`, `createElement`,
`createText`, `appendChild`, `setNodeAttribute`, `insertBefore`,
`removeChild`, `parentNode`, and `firstChild` — both the mount half a
reconciler needs and the patch half (move, replace, remove, and read the
tree to decide). Nodes cross into script as opaque numeric handles, bounds-
checked against the live document before every use. What React's renderer
would still need beyond this: `nextSibling`, the property/style interfaces
(a node's computed style, `classList`, `dataset`), and the live node
identity to stop being a numeric handle a script could reuse against a
stale document (mitigated today by the bounds check, not eliminated by a
stronger identity model).

### Event loop and scheduling

React schedules work on microtasks and, in concurrent mode, on a cooperative
scheduler. The engine has a microtask queue now — `queueMicrotask(fn)` is a
VM-native builtin, queued functions run after the triggering script returns
and before control returns to the embedder, one at a time, including further
tasks queued during draining. What it is not: a *scheduler*. There is still
exactly one script execution at a time, no timers, and no task-vs-microtask
distinction — the primitive a runtime needs to defer work exists; the
cooperative, priority-aware scheduler concurrent-mode React needs does not.

### Module loading and app entry

A bundled app is a module graph with an entry point. The engine has no
module loader; scripts are inline `<script>` text compiled in isolation.

## The milestone ladder

Each rung is independently useful and testable, and each is the smallest
step that unlocks the next. The early rungs are ungated engine work; the
later ones reach decisions the owner still holds (a production JS security
posture, `WP-019`; the trusted-chrome authority for a system UI, `WP-004`).

- **APP-0 — Framework SSR output.** *Done.* Static server-rendered HTML/CSS
  renders through the normal pipeline. Proven by the dashboard fixture.
- **APP-1 — Arrays in `turing-js`.** *Done.* Array literals, indexing,
  `length`, index-write growth, nesting with objects, spec-correct
  truthiness; holes and spread refused. Arrays are represented as objects
  with a `length` property, which is the specification's own model, so they
  reuse the entire object heap and collector. The smallest self-contained
  step toward `createElement(type, props, ...children)` and children arrays.
- **APP-2 — Function values, then closures.** *First-class function values
  done; capture pending.* Anonymous function expressions are now values —
  stored, passed, returned, and called indirectly (`f()`, `fs[0]()`,
  `apply(g, v)`), with arity and type checks. What they do **not** yet do is
  capture an enclosing local: a reference to one is refused as undefined at
  compile time rather than captured, because by-value capture would compute
  silently-wrong values for the closure-over-mutation patterns React relies
  on, and by-reference capture is a larger VM change (indirect calls exist
  now; a shared-cell environment does not). So function values landed as a
  correct whole, and true capture — the closure — is the next increment on
  the same machinery. Arrow-function syntax — `x => x + 1`, `(a, b) => ...`, `() => {...}` — is
  sugar over this same machinery. Closures now **capture enclosing `const`
  bindings** by value — correct by construction, because a const cannot
  change, so the snapshot can never be observed wrong. This is the dominant
  real pattern (a callback closing over const props/state). Capturing a
  mutable `let`/`var` (by-reference cells) and multi-level capture are
  refused, not computed wrong, and are the remaining pieces of full
  closures.
- **APP-3 — DOM construction bindings.** *Done.* `documentBody`,
  `createElement`, `createText`, `appendChild`, and `setNodeAttribute` bound
  to script, with nodes crossing the boundary as opaque numeric handles (arena
  indices, treated by the interpreter as plain numbers, never as heap
  pointers). A script now builds a subtree the way a framework renderer does,
  and the engine lays it out and paints it — proven by
  `benchmarks/corpus/framework-output/script-built-ui.html`, whose entire UI
  is constructed by a loop calling these operations. The *patch* half a
  reconciler also needs — `insertBefore`, `removeChild`, `parentNode`,
  `firstChild` — is bound too, so a script can move, replace, and remove
  nodes and read the tree to decide, not only mount.
- **APP-4 — A microtask queue.** *Done.* `queueMicrotask(fn)` is a
  VM-native builtin — it cannot be a host operation, since it must reach the
  interpreter's own queue, which a `Host` implementation has no access to.
  Queued functions and closures run after the currently executing top-level
  call finishes and before control returns to the embedder, one at a time,
  including further tasks queued during draining — the defining property of
  a microtask queue, not a single batch pass. Proven with a script that
  builds one DOM node synchronously and a second inside a queued microtask;
  both are present by the time `Page::load` returns
  (`crates/turing-engine/tests/pipeline.rs`). A queued closure is rooted
  through a collection before it runs, verified by a regression test that
  fails without that rooting (a real use-after-free the collector's own
  generation check caught rather than corrupting memory). This is not a
  cooperative *scheduler* — there is still exactly one script execution at a
  time, no timers, no task-vs-microtask distinction — but it is the minimal
  primitive a runtime needs to schedule work after the script that triggered
  it returns, which is what the milestone asked for.
- **APP-5 — A tiny reconciler on the engine.** *Demonstrated.* A minimal
  React-like runtime — virtual nodes, a recursive `render`, and components
  that are closures capturing const props — written entirely in the engine's
  own JavaScript subset, produces real DOM the engine lays out and paints
  (`benchmarks/corpus/framework-output/mini-react-runtime.html`, with a
  pipeline test). This proves the language features and DOM bindings compose
  into the createElement-over-components shape, which is the shape the real
  runtime needs. It is a demonstration of composition, not the real React
  runtime (APP-6), which additionally needs mutable capture, an event loop,
  and a great deal more of the language.
- **APP-6 — The real React runtime, then a bundler's output.** The bounded
  development proof should use the researched esbuild + Preact compatibility
  path inside the Servo page surface. This is explicitly a source-fidelity
  and engine-integration experiment, not approval to put Preact, React DOM, or
  a page DOM in trusted release chrome. See the [JSX runtime compiler
  selection](../research/jsx-runtime-compiler-selection-2026-07.md).
- **APP-7 — The Nova source rendered by the engine.** The chrome, and then
  the system interface, rendered by running its own React rather than by the
  Rust interim.

## What does not change

- **The independent-engine boundary holds.** No Chromium/Blink/V8/Electron
  in any release path (`AGENTS.md`). "Electron-class" describes the *product
  capability*, never the implementation.
- **Security is not deferred to make this work.** Running arbitrary
  framework JavaScript is exactly the hostile-input surface the security
  book governs; the JS-hardening and trusted-chrome gates (`WP-019`,
  `WP-004`) apply in full, and [Chromium as a security
  reference](../security-engine/reference-chromium-security.md) is the
  calibration for what running untrusted app code must survive.
- **No completion claim.** This is the order of work, not a promise of
  arrival. Every rung lands with evidence or it has not landed.
