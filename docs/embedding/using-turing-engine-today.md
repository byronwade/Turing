# Using `turing-engine` today

Status: describes the real, current library API
Companion to: [`README.md`](README.md), which describes the *design target*
(`Engine`/`Profile`/`View`, a C ABI, generated multi-language SDKs) — none of
that exists yet. This document is the other half: what a Rust program can
actually depend on and call right now.

Everything below is exercised by
[`crates/turing-engine/examples/embed_minimal.rs`](../../crates/turing-engine/examples/embed_minimal.rs).
Run it with:

```
cargo run -p turing-engine --example embed_minimal
```

## The one type: `Page`

`turing_engine::Page` is the whole public surface. There is no separate
engine/profile/view split, no async runtime, no capability tokens — a `Page`
owns one parsed, styled, laid-out document and every operation is a plain
synchronous method call.

```rust
use turing_engine::Page;

let mut page = Page::load(html, viewport_width)?;
```

`Page::load` parses the HTML, cascades the CSS, runs every `<script>` once
against the live document, and lays out — one call, one `Result`. There is no
separate "now render" step required before the page is queryable or paintable.

## What you can do with a loaded page

| Method | What it answers |
|---|---|
| `page.title()` | the document's `<title>`, if any |
| `page.content_height()` | total laid-out content height in CSS px |
| `page.dom()` | the live `turing_dom::Dom` — read attributes, walk nodes |
| `page.layout()` | the root `LayoutBox` — geometry for every element |
| `page.display_list()` | the paint-ready display list, pre-rasterization |
| `page.render(width, height)` | rasterizes onto a `Canvas` (a plain sRGB pixel buffer; `Canvas::pixel(x, y)` reads one pixel back) |
| `page.render_scrolled(...)` | same, offset by a scroll position |
| `page.resize(new_width)` | re-lays-out at a new viewport width |
| `page.target_at(point)` | hit-tests: which `NodeId`, if any, is under this point |
| `page.dispatch_at(point, &event)` | routes an event through capture/target/bubble, runs whatever script listeners it finds, and **relays out automatically if the listener mutated the DOM** |
| `page.run_script(source)` | runs arbitrary script against the live document immediately |

The property that makes this usable as an embedding surface is that
`dispatch_at` never leaves the caller responsible for remembering to re-layout
or re-render after a mutation — the very next `render` call already reflects
whatever the click changed. `embed_minimal.rs` proves this directly: it reads
a pixel before a simulated click, dispatches the click, reads the same pixel
after, and asserts the two differ.

## What this is not

This is a library API for one process to embed one page — not the
[`README.md`](README.md) design target's Engine/Profile/View lifecycle, not a
stable C ABI, not a generated multi-language SDK, and not a security/process
isolation boundary. There is exactly one `Page`, one thread, one trust domain.
Treat this document as "what exists to build on today"; treat `README.md` as
the direction that surface would need to grow in before an untrusted or
cross-language embedder could depend on it.

## A note on pixel sampling

If you write your own probe against `render()`'s output, sample a point that
is actually on the element's *background*, not on rendered text. Turing's
current text painter draws glyphs from an 8×8 bitmap font directly on top of
the background fill; a sample point that lands on a glyph stroke reads the
text's foreground color, not the element's background — this looks like a
CSS or paint bug but isn't one. `embed_minimal.rs` samples `(200, 5)` rather
than a point inside the "Click me" label for exactly this reason.
