# Competitive Browser and Engine Studies

Status: active comparative research baseline  
Owner: research, architecture, product, and developer experience  
Relationship to normative design: recommendations remain non-normative until accepted in the owning Blueprint chapter or ADR.

This book separates engine architecture from browser-product design. Chromium/Blink/V8, WebKit/JavaScriptCore, Gecko/SpiderMonkey, Servo, and Ladybird are studied as engine and runtime references. Brave, Arc, Zen, Orion, Safari, and related products are studied for user experience, workflow, privacy, distribution, and maintainership lessons without treating a browser shell as an independent engine.

## Reading order

1. [Chromium, Blink, and V8](01-chromium-blink-v8.md)
2. [WebKit and JavaScriptCore](02-webkit-javascriptcore.md)
3. [Gecko and SpiderMonkey](03-gecko-spidermonkey.md)
4. [Servo](04-servo.md)
5. [Ladybird](05-ladybird.md)
6. [Browser products: Brave, Arc, Zen, Orion, and Safari](06-browser-products.md)
7. [Comparison scorecard and adoption rules](07-comparison-scorecard-and-adoption-rules.md)

## Comparative method

Each study distinguishes:

- official documented architecture;
- observable product behavior;
- open-source/license/governance facts;
- hypotheses that require measurement;
- lessons Turing may prototype;
- patterns Turing should not copy blindly;
- unresolved questions and falsifiable experiments.

No document ranks engines by speed, memory, energy, security, or compatibility without fixed-hardware equivalent measurement. Source code may be studied for interoperability and architecture under its license, but Turing does not copy implementation code or use an existing engine in release paths.

## What leadership means

Turing's target is the Pareto frontier across open-web compatibility, interaction latency, memory, energy, security, accessibility, recovery, developer API quality, observability, everyday usability, and open-source sustainability. A benchmark win with a smaller feature set, weaker isolation, hidden tab discard, or omitted failures is invalid.

## Related material

- [Browser engine landscape report](../research/browser-engine-landscape-2026-07.md)
- [Research and measurement program](../blueprint-v1/22-research-program.md)
- [Browser engine book](../engine/README.md)
- [Developer experience book](../developer-experience/README.md)
- [Performance engineering book](../performance/README.md)

<!-- MARKET-STRATEGY-2026-07 -->
## Market-gap companion

The [browser market-gap report](../research/browser-market-gap-2026-07.md) compares product workflows and user-demand signals. Competitive studies remain separate from engine conformance and do not authorize copying proprietary implementation or branding.
