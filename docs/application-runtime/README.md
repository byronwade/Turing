# Turing as an Application Runtime

Status: architecture and milestone research. Owner: @byronwade (product
direction), engine and UI-runtime owners. Opened 2026-07-20 by owner
direction.

/ This book does not claim the runtime exists. It states the target, the
honest gap from today's engine, and the order the gap can be closed in. /

## The target

Turing is not only a web browser. The owner's direction is that the Turing
engine become an **application runtime** — the way Electron lets a product
ship a React/Next.js/TanStack application as a desktop app, except that the
rendering engine is Turing's own, built from scratch, with no Chromium,
Blink, or V8 underneath.

Two concrete ambitions define the target:

1. **The system UI is the engine's own output.** The Nova design
   (`docs/ui-runtime/design-lab/turing-nova-design-source.jsx`) is React.
   The end state is that the engine *runs that React* and the running
   result **is** the browser's chrome and, further out, the desktop system
   interface — not a hand-port of Nova into Rust display lists. Today's
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

## The honest gap

Running a framework's *client* runtime — hydration, hooks, reconciliation,
event handlers — needs engine capability that does not exist yet. Named
plainly rather than glossed:

### JavaScript (`turing-js`)

The interpreter is a deliberately bounded subset: numbers, strings,
booleans, `null`/`undefined`, bindings, arithmetic and logic, control flow,
function declarations, calls, recursion, **and objects with property
access**. It refuses — by design, at compile time — the constructs a React
runtime is built from:

- **arrays** (children are arrays; `.map` over children is everywhere);
- **closures and function expressions / arrow functions** (hooks close over
  state; every JSX event handler is a closure);
- **`class`** (older React components, many libraries);
- **prototypes and `this` semantics**;
- **`try`/`catch`**, **`async`/`await`**, **generators**, **modules**,
  **regular expressions**.

This is the largest gap, and it is the load-bearing one. It is also already
a planned program, not a new one: `docs/blueprint-v1/06-javascript-runtime.md`
and the `docs/javascript/` book scope a full from-scratch ECMAScript engine —
parser, bytecode interpreter, generational GC, baseline and optimizing JIT,
Web IDL bindings, WebAssembly, and an event loop — explicitly "capable enough
to eventually run React's runtime as web content." What this book adds is a
*reason to prioritise that program toward framework support*, and a rung
order for it. The engine's governing principle is a strength for this goal,
not a weakness: a partially implemented language computes wrong values
silently, so every unimplemented construct is refused visibly. The runtime
grows one honest construct at a time, and everything that runs stays
trustworthy.

### DOM API surface

`turing-webidl` binds a small capability set: `getAttribute`, `setAttribute`,
`removeAttribute`, `tagName`, `hasElement`, `textContent`,
`addEventListener`. React's renderer needs more — `createElement`,
`createTextNode`, `appendChild`, `insertBefore`, `removeChild`, `parentNode`,
`nextSibling`, node identity that crosses into script, and the property/style
interfaces. The DOM crate already has the *operations* (create, append,
insert, remove, mutation epochs); the gap is binding them to script with
live node identity rather than the current id-string indirection.

### Event loop and scheduling

React schedules work on microtasks and, in concurrent mode, on a cooperative
scheduler. The engine has no event loop, microtask queue, or timer yet.
Script runs once, synchronously, on load or on an input dispatch.

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
- **APP-4 — A microtask queue and a minimal scheduler.** Enough of an event
  loop for a runtime to flush work after an event.
- **APP-5 — A tiny reconciler on the engine.** Prove the shape end to end
  with a hand-written minimal React-like runtime before pulling in the real
  one — the same "reference implementation first" discipline the rest of the
  engine follows.
- **APP-6 — The real React runtime, then a bundler's output.** Load
  framework-emitted JS and run it.
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
