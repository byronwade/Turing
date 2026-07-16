# CSS, Cascade, Selectors, and Invalidation

Status: research baseline; selector and style representations remain experimental  
Owner: style system  
Purpose: Define a standards-correct style system whose common cases are compact and fast while dependency tracking keeps mutation cost explainable.

## Relationship to the Turing program

This document is subordinate to [Blueprint 05](../blueprint-v1/05-web-engine.md) and must coordinate with layout, animation scheduling, accessibility, and DevTools.

## Parsing and rule storage

CSS parsing preserves forward-compatible error handling. Stylesheets are immutable after construction where possible and hold compact rule/value data plus optional source ranges for DevTools. Parsed rule trees are partitioned by origin, tree scope, layer order, media/container environment, and profile policy.

Values use typed representations after parsing. Custom properties retain token streams and dependency edges because substitution occurs later. Unknown declarations and unsupported at-rules follow specification recovery rather than aborting the sheet.

## Selector compilation

Selectors compile into match programs organized from the rightmost compound selector. Candidate indexes may use ID, class, local name, attribute presence, pseudo-state, and universal buckets. Fast rejection structures are hints only.

The compiled form records dependencies on ancestors, siblings, descendants, states, attributes, namespaces, shadow boundaries, scopes, and relational selectors such as `:has()`. Matching has explicit recursion/work limits and reports pathological selectors rather than hanging the renderer.

## Cascade and computed values

The cascade implementation makes origin, importance, encapsulation, layers, specificity, scope proximity, and source order explicit. Computed style is assembled from immutable shared blocks for common groups—font, color, box, text, effects, SVG—while rare values live in side storage.

Dependency metadata records inherited values, custom-property graphs, viewport and container units, root style, fonts, environment variables, user preferences, animations, and visited-link privacy state. Style sharing requires a proof-oriented key; uncertain cases do not share.

## Invalidation architecture

Every selector and computed-value dependency contributes to an invalidation plan. Mutation classification includes:

- attribute, class, ID, state, and pseudo-state changes;
- child-list and sibling-order changes;
- subtree insertion/removal and shadow slot changes;
- viewport, zoom, media feature, preference, and font changes;
- container size/style changes;
- animation and transition ticks;
- stylesheet, layer, scope, and adopted-sheet changes.

Invalidation plans choose a safe root and record why broader work was required. Full rematch and full computed-style rebuild remain test oracles.

## Animations and transitions

Animation sampling is separated from base style. Compositor-eligible properties are promoted only when interpolation, property-tree state, and resource budgets permit. Main-thread animation dependencies are visible.

Transition creation observes before/after computed values without retaining entire historical style graphs. Reduced-motion policy, background throttling, lifecycle freeze, and document visibility are integrated without changing specified event ordering.

## Developer observability

DevTools should explain the winning declaration, all losing declarations, cascade layer/scope, inherited source, custom-property chain, computed-value dependencies, style-sharing decision, and invalidation cause. Cost views report selector candidates, match counts, rematch roots, cache hits, and style bytes by document.

## Non-negotiable invariants

- Fast rejection and style sharing can skip work but cannot change matching or computed values.
- Visited-link and other privacy-sensitive states never leak through computed-style or protocol output.
- Custom-property cycles and expansion are bounded and standards-correct.
- Incremental style equals a full rebuild for DOM, layout, paint, accessibility, and script-visible results.
- Unsupported CSS is ignored or preserved according to parsing rules, never reinterpreted as a proprietary shortcut.

## Required evidence

- Pinned WPT results by CSS module and feature.
- Generated mutation sequences comparing incremental and full style computation.
- Selector corpus benchmarks reporting candidates, matches, invalidation breadth, allocations, and tail latency.
- DevTools golden traces for cascade, variables, container queries, shadow scopes, and `:has()`.
- Privacy tests for visited links, system colors, fonts, media features, and forced colors.

## Known risks and unresolved questions

- Overly precise dependency graphs may cost more memory than conservative invalidation saves.
- Aggressive style sharing can create rare, difficult correctness failures.
- Container queries and relational selectors create feedback and broad invalidation pressure.
- Source preservation for DevTools can dominate stylesheet memory.

## Primary sources

- CSS Working Group drafts — https://drafts.csswg.org/
- Chromium RenderingNG architecture — https://developer.chrome.com/docs/chromium/renderingng-architecture
- Chromium RenderingNG key data structures — https://developer.chrome.com/docs/chromium/renderingng-data-structures
- Chromium LayoutNG — https://developer.chrome.com/docs/chromium/layoutng
- Web Platform Tests — https://web-platform-tests.org/
- W3C Web Platform Design Principles — https://www.w3.org/TR/design-principles/

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
