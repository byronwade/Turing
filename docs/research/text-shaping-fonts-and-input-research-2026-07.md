# Text Shaping, Fonts, and Input Research - July 2026

Status: deferred `RQ-06` no-claim research packet
Owner: text, fonts, internationalization, platform, accessibility, input, security, and performance
Research date: 2026-07-19
Confidence: high for the standards and shaping-library observations; low for any Turing text stack, font policy, rasterization, or performance conclusion until corpus and platform evidence exist

## Question

Which text stack balances Unicode correctness, shaping quality, font fallback, raster and platform consistency, accessibility, IME behavior, memory, and performance across supported platforms?

## Why This Matters

Text is simultaneously web content, a security-sensitive parser input, a layout dependency, a glyph and font resource, an accessibility representation, and a user input surface. A fast Latin-only path cannot establish browser text correctness. A platform-native path may improve integration while creating cross-platform differences, font-availability drift, or inconsistent metrics. A single shaping library may still require explicit bidirectional, line-breaking, fallback, raster, IME, and accessibility policy.

This packet defines a deferred research route for `RQ-06`. It does not select HarfBuzz, ICU, a Rust text stack, DirectWrite, CoreText, Uniscribe, a rasterizer, a font policy, or an IME architecture.

## Source-backed observations

### Bidirectional ordering is algorithmic and paragraph-sensitive

Unicode UAX #9 defines the Unicode Bidirectional Algorithm as a multi-phase process applied to paragraphs. Direction, embedding, overrides, isolates, and character classes affect visual ordering. A text pipeline must preserve logical text, directional metadata, clusters, caret mapping, hit testing, and accessibility order separately from visual glyph order.

Source: [Unicode UAX #9: Unicode Bidirectional Algorithm](https://unicode.org/reports/tr9/), retrieved 2026-07-19.

### Line breaking is contextual and partly tailorable

Unicode UAX #14 defines break opportunities and a rule system, while noting that actual line selection depends on width, display, and higher-level policy. CSS Text defines browser-visible whitespace, line-breaking, justification, alignment, and text-transformation processing. A line-break implementation therefore needs both Unicode data and CSS/layout context; a character-only table is not a complete browser implementation.

Sources: [Unicode UAX #14: Unicode Line Breaking Algorithm](https://www.unicode.org/reports/tr14/), [W3C CSS Text Module Level 3](https://www.w3.org/TR/css-text-3/), retrieved 2026-07-19.

### Shaping consumes script, language, direction, font, and feature state

The HarfBuzz manual describes shaping as transforming Unicode codepoints into positioned glyphs and identifies buffer direction, script, language, font features, and text-run boundaries as shaping inputs. It also documents shape plans and caching. These inputs must be part of any cache key and invalidation record; caching only by text bytes risks incorrect output.

Sources: [HarfBuzz manual](https://harfbuzz.github.io/), [HarfBuzz shaping API](https://harfbuzz.github.io/harfbuzz-hb-shape.html), retrieved 2026-07-19.

### Font and platform integration is a separate boundary

HarfBuzz documents integrations with platform and font backends, while its shaping output is glyph and position data rather than a complete browser text stack. Font discovery, permissions, variation axes, fallback, emoji/color formats, rasterization, hinting, and platform text input remain separate decisions. A shaping-library choice does not settle those questions.

## Candidate stack boundaries

The owner-approved comparison should keep these boundaries explicit:

1. Unicode data and segmentation: character properties, bidi, line breaking, grapheme/caret boundaries, normalization policy, and version pinning.
2. Shaping: script/language/direction runs, OpenType/AAT/Graphite behavior, cluster mapping, features, variable fonts, and shape-plan caching.
3. Font selection and fallback: origin/profile permissions, local fonts, web fonts, fallback order, missing glyphs, emoji/color fonts, variation axes, and privacy limits.
4. Metrics and layout: glyph advances, kerning, line boxes, justification, hyphenation, vertical text, writing modes, ruby, selection, hit testing, and bidi caret mapping.
5. Raster and display: glyph atlas lifetime, hinting, antialiasing, subpixel policy, color management, GPU/software fallback, and deterministic screenshot limits.
6. Input and accessibility: IME composition, dead keys, candidate windows, selection, clipboard boundaries, screen-reader text/range mapping, and platform accessibility APIs.

This decomposition is a research model, not a selected architecture.

## Evidence required before a text-stack decision

The owner-approved package should provide:

- a versioned Unicode and font corpus covering Latin, Greek, Cyrillic, Arabic, Hebrew, Indic, Southeast Asian, CJK, Hangul, combining marks, emoji, symbols, vertical text, and mixed-direction documents;
- bidi isolates, overrides, nested embeddings, mirrored characters, mixed scripts, and visual/logical selection fixtures;
- line-breaking, white-space, justification, hyphenation, ruby, vertical-writing, and CSS text-property cases;
- font fallback, missing glyph, variable-font, color-font, web-font, local-font, permissions, and font-load-failure fixtures;
- shaping outputs with glyph IDs, clusters, advances, offsets, direction, script, language, feature set, and exact font identity;
- raster fixtures separated from shaping fixtures, with platform, renderer, scale, color, antialiasing, and nondeterminism policy;
- IME, dead-key, composition, selection, deletion, clipboard, and candidate-window workflows on each supported platform;
- accessibility-tree, range, name/value, caret, and screen-reader mappings that remain correct under bidi and fallback;
- security and privacy tests for font parsing, remote fonts, local-font exposure, origin isolation, and untrusted font data;
- independent review of Unicode/font licenses, update cadence, provenance, fuzzing, and platform support.

## Measurement plan

Measure separate distributions for:

- segmentation, bidi, line-break, shaping, fallback, font-load, layout, raster, and display time;
- cold and warm shape-plan/font/cache behavior, cache bytes, eviction, and invalidation;
- memory and allocations by Unicode data, font data, shape plans, glyph buffers, atlases, and platform handles;
- keystroke-to-composition, composition-to-layout, caret movement, selection, and screen-reader update latency;
- frame pacing and input latency during long multilingual pages, animation, editing, zoom, and font replacement;
- missing-font, malformed-font, unsupported-script, timeout, cancellation, crash, and software-fallback denominators;
- cross-platform metric and raster differences, with semantic equivalence separated from pixel equivalence.

No comparison may disable accessibility, use a Latin-only corpus, treat platform-specific raster pixels as semantic failure without policy, or hide font-load and IME failures.

## Rejection rules

Reject the packet as decision evidence when it:

- treats UTF-8 decoding or Unicode codepoint iteration as complete text shaping;
- caches shaping without script, language, direction, font, feature, variation, and text-run identity;
- validates only screenshots and ignores clusters, caret mapping, bidi order, accessibility, or IME behavior;
- claims a platform API or shaping library is a complete text stack;
- uses undisclosed local fonts, network fonts, font versions, raster settings, or fallback behavior;
- omits malformed/untrusted font handling, remote-font privacy, or cancellation and failure cases;
- compares speed on Latin-only or pre-shaped text while excluding complex scripts and user input;
- treats platform differences as either universally acceptable or universally incorrect without an explicit support policy.

## Current status and next proof

`RQ-06` remains deferred outside the active pre-build crosswalk. The next proof is an owner-approved Unicode/font/IME corpus and version manifest, followed by shaping, line-break, fallback, accessibility, and platform-input oracle fixtures. No text stack, font policy, raster policy, compatibility result, accessibility result, performance result, or readiness claim follows from this packet.

## Claim boundary

This is source-backed research preparation only. It does not select a shaping engine, Unicode version, font backend, fallback policy, rasterizer, IME architecture, accessibility adapter, platform text API, performance target, or production support claim.
