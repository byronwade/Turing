# Text, Fonts, and Internationalization

Status: research baseline; platform text strategy requires measurement  
Owner: text and internationalization  
Purpose: Treat text as a core engine subsystem spanning Unicode, font selection, shaping, line layout, editing, accessibility, privacy, and platform integration.

## Relationship to the Turing program

This document refines the text section of [Blueprint 05](../blueprint-v1/05-web-engine.md) and coordinates with accessibility and privacy.

## Text pipeline

Text processing stages are explicit:

1. DOM text and CSS white-space/text-transform handling;
2. grapheme, word, sentence, and line-break segmentation;
3. bidi paragraph and run resolution;
4. script/language itemization and font fallback;
5. shaping with OpenType features, variation axes, kerning, and cluster mapping;
6. line breaking, hyphenation, justification, ruby, vertical writing, and decoration;
7. glyph rasterization and color-font composition;
8. caret, selection, hit-test, accessibility, and editing geometry.

Each stage preserves source-to-cluster mappings and uses bounded buffers.

## Font selection and fallback

Turing owns CSS font matching, generic-family policy, fallback order, downloadable-font state, metric overrides, privacy behavior, and cache accounting. Platform APIs or HarfBuzz/FreeType may implement shaping and rasterization behind reviewed adapters.

Font identity includes source, face index, variation coordinates, synthesis policy, feature settings, optical sizing, size, scale, and platform raster mode. System font enumeration is not exposed beyond web standards and privacy policy.

## Caches and lifecycle

Font metadata, faces, shaped runs, glyphs, and atlases have separate caches and budgets. Keys include all semantic inputs. Shared resources respect profile and private-session boundaries. Pressure can evict raster or shaping data without invalidating layout semantics; metric-affecting changes advance the appropriate epochs.

Web-font completion may trigger relayout. The engine limits repeated metric churn and records layout shifts attributable to fonts.

## Editing and input methods

IME composition, dead keys, complex scripts, bidirectional selection, grapheme navigation, vertical writing, password fields, spellcheck, dictation, and accessibility actions use platform adapters without surrendering DOM/editing semantics.

Selection is stored as logical document positions with affinity and mapped to fragment geometry per epoch. Clipboard and drag data pass through sanitization and origin/profile policy.

## Privacy and fingerprinting

Font availability, glyph metrics, antialiasing, locale, time zone, language lists, and text measurement can reveal identifying information. Turing should minimize entropy through bounded font exposure, partitioning, standardization, permission or user-selected flows where appropriate, and clear private-mode behavior.

Developer diagnostics may reveal additional local detail only under an explicit local grant and must not leak through page APIs.

## Cross-platform consistency

Correct text does not require identical pixels on every operating system. Semantic gates prioritize code-point/cluster mapping, line-break opportunities, glyph coverage, layout geometry within declared tolerances, selection behavior, and accessibility ranges. Pixel tests pin fonts and raster settings where exact comparison is required.

## Non-negotiable invariants

- Text is never split or navigated at arbitrary byte boundaries.
- Bidi, shaping, selection, accessibility, and hit testing use consistent cluster mapping.
- Untrusted font data is parsed and shaped behind strict limits and isolation.
- Font caches are partition-aware and cannot become cross-profile tracking channels.
- Platform differences are documented rather than hidden under broad test exemptions.

## Required evidence

- Multilingual corpus covering major scripts, bidi, vertical writing, emoji, variable/color fonts, ruby, and combining marks.
- UAX, CSS, HTML, accessibility, and WPT conformance results.
- IME and assistive-technology manual matrices on every supported platform.
- Shaping/raster adapter comparison for latency, memory, compatibility, and deterministic geometry.
- Font parser/shaper fuzzing, malformed-table limits, and process-containment tests.

## Known risks and unresolved questions

- Fallback and platform font differences can produce persistent compatibility gaps.
- Font parsing and shaping libraries create a large native attack surface.
- Metric-compatible privacy defenses may reduce typographic fidelity.
- Text cache keys can grow large or omit rare semantic inputs.

## Primary sources

- Unicode Standard Annexes — https://www.unicode.org/reports/
- Unicode Bidirectional Algorithm — https://unicode.org/reports/tr9/
- HarfBuzz manual — https://harfbuzz.github.io/
- FreeType documentation — https://freetype.org/freetype2/docs/
- CSS Working Group drafts — https://drafts.csswg.org/
- WAI-ARIA — https://www.w3.org/TR/wai-aria/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
