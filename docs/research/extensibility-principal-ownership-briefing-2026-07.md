# Extensibility Principal Ownership Briefing - July 2026

Status: checked decision-support briefing; no ruling made, no book rescoped
Owner: Plug-in platform, extension, enterprise, product, and architecture owners
Related decision: `ADR-0011`
Prepared: 2026-07-20

## Question

The `plugins` and `extensions-enterprise` books describe the same extensibility surface using different first-class principals and do not cross-reference each other. Which book owns the principal?

## Short answer

The question is not symmetric, and framing it as "which book wins" obscures the cause.

The two books diverge because one of them adopts the vocabulary of `ADR-0011`, which is **proposed**, not accepted. Resolving the divergence is therefore downstream of an ADR decision rather than an editorial preference between two teams.

## What each book asserts

The [Plug-in platform book](../plugins/README.md) states: "Turing calls extensibility units **Plug-ins**. Every Plug-in -- including first-party packages -- is an untrusted, separately identified, revocable, resource-bounded principal." It defines Tier A through Tier D, placing portable WebAssembly components with WIT imports at Tier B and a "restricted WebExtensions compatibility adapter with a published API matrix" at Tier C, explicitly noting that Tier C "does not define native Turing APIs".

The [extensions/enterprise book](../extensions-enterprise/README.md) treats extensions as the first-class principal. Five of its seven chapters are extension-centric: extension processes and isolated worlds, permissions and host grants, event-driven background work, declarative network rules and native messaging, and extension updates and DevTools access. The remaining two cover enterprise policy and accounts/sync.

## What the normative records say

This is the part that decides the shape of the question.

[`ADR-0011` — Capability-based Turing Plug-ins](../blueprint-v1/17-architecture-decisions.md) has status **proposed**: "Prefer WIT/WebAssembly components, isolate WebExtensions, and prohibit ambient authority/native code." It is not accepted.

The Blueprint chapter that `extensions-enterprise` names as its canonical overview, [Capability Parity §8](../blueprint-v1/02-capability-parity.md), frames the target in extension terms: "a documented WebExtensions compatibility layer, beginning with a deliberately small Manifest V3-style subset", with required areas enumerated as extension APIs. It does not use the Plug-in principal or the tier model.

So the currently normative framing is the extension-centric one. The Plug-in principal, the tier model, and the demotion of WebExtensions to a restricted Tier C adapter are all `ADR-0011`'s proposal, described in the Plug-in book as settled vocabulary.

## What this is and is not

It is not a readiness overclaim. The Plug-in book's status line is honest: "architecture and product research; no Plug-in runtime or store exists." No implementation, security, or compatibility claim is being made.

It is a vocabulary divergence in which one book writes a proposed architecture as the project's established terminology, while the normative Blueprint chapter still uses the other. A reader following the documented reading order encounters the extension-centric Blueprint framing, then a book that declares a different principal without noting that the difference rests on an unaccepted ADR.

## The options

| | What it means | Cost |
|---|---|---|
| **1. Cross-reference only** | Both books stand; each states that the principal question is open pending `ADR-0011`, and links the other. | Cheapest and immediately available. Leaves two vocabularies in the documentation, which is honest but adds reader load. |
| **2. Scope `extensions-enterprise` to enterprise, accounts, and sync** | Move extension-principal material under `plugins` Tier C, leaving enterprise policy and accounts/sync in place. | Substantial rewrite of five chapters, and it presumes the `ADR-0011` outcome before the ADR is accepted. |
| **3. Treat the Plug-in model as proposed vocabulary** | The `plugins` book marks its naming and tier model as `ADR-0011`-dependent; `extensions-enterprise` remains aligned with the normative Blueprint until the ADR is accepted. | Small edit. Matches the current record. Defers structure to the ADR, which is where it belongs. |
| **4. Accept `ADR-0011` first, then restructure** | Rule on the ADR, then rescope both books to the accepted model in one change. | Correct end state, but blocked on the same owner-decision capacity as every other gate. |

## Analytical recommendation, not an approval

**Option 3 now, Option 4 later.** Marking the Plug-in book's principal and tier model as `ADR-0011`-dependent costs one edit, removes the appearance that the naming is settled, and leaves the restructure to the decision that should own it. Option 1 is a reasonable weaker form of the same move. Option 2 should be rejected: it commits to the ADR's outcome through documentation structure rather than through the ADR.

This is analysis of documented trade-offs. It does not rule, does not rescope either book, and does not accept or reject `ADR-0011`.

## Why this was not fixed directly

Earlier passes on 2026-07-20 corrected factual defects — wrong identifiers, stale counts, dead links, mismatched statuses — without owner input, because each had a single verifiable right answer in a machine registry. This does not. Which book owns a principal is a documentation-architecture decision with no registry to check it against, and the underlying ADR is unaccepted. An agent restructuring five chapters here would be deciding `ADR-0011` by editorial action.

## Current disposition and next proof

No ruling exists. Both books stand as written, and this is the last open item on the coherence surface examined on 2026-07-20. The next proof is either the small `ADR-0011`-dependency edit under option 3, or an `ADR-0011` decision.

## Claim boundary

This briefing is decision support only. It does not select an extensibility principal, rescope any book, accept or reject `ADR-0011`, approve a Plug-in tier model, or support any implementation, compatibility, security, ecosystem, or readiness claim.
