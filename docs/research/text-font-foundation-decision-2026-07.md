# Text-font foundation decision — reference glyph set (2026-07)

Status: accepted for the CPU reference rasterizer only. Owner: @byronwade.
Recorded from the owner's 2026-07-20 direction to produce a working, visible
browser application; that direction is what resolves the previously open
`text-font-foundation-review` gate on `WP-009` for this bounded scope.

## Decision

The CPU reference rasterizer (`crates/turing-raster`, `COMP-017`) draws
`DisplayItem::Text` using an embedded 8x8 monochrome bitmap font covering
exactly the ninety-five printable ASCII characters. Characters outside that
range draw a hollow replacement box so missing coverage stays visible.

The glyph data is the printable-ASCII range of `font8x8_basic` from Daniel
Hepper's `font8x8` collection, derived from Marcel Sondaar's public-domain VGA
fonts. Both publications are explicitly public domain; provenance and encoding
are documented in `crates/turing-raster/src/font.rs`. The data is embedded
source, not a runtime dependency: no crate, no build script, no fetched file.

## Why this resolves the gate for this scope

The gate was held open because inventing a glyph representation would have
preempted an owner decision (`docs/research-log.md`, 2026-07-20 CPU reference
rasterizer entry). The owner has now directed that the engine produce visible,
readable output. A public-domain bitmap font is the smallest decision that
satisfies that direction: it adds no dependency, no license obligation, no
shaping machinery, and it agrees by construction with the existing
`turing_layout::TextMetrics` default of an 8-wide advance.

## What this deliberately does not decide

- The product font stack: shaping, hinting, subpixel rendering, font loading,
  fallback chains, and web fonts are all future Foundation-class dependency
  decisions under `docs/blueprint-v1/03-language-and-dependency-strategy.md`.
- Unicode coverage. The reference set is printable ASCII; everything else is
  visibly a placeholder, never silently dropped.
- Any performance posture. The reference painter remains the
  written-to-be-read implementation faster painters are diffed against.

If a later owner decision selects a real text stack, this glyph set stays as
the reference painter's fallback so the diff baseline remains dependency-free.
