# JavaScript Values, Objects, Shapes, and Inline Caches

Status: research and design baseline  
Owner: JavaScript object model  
Purpose: Define compact observable semantics and optimization metadata without making representations part of the language contract.

## Relationship to the Turing program

This document expands the runtime object-model portion of [Blueprint 06](../blueprint-v1/06-javascript-runtime.md). The collector owns object liveness as described in [Garbage collection and host lifetimes](03-garbage-collection-and-host-lifetimes.md).

## Tagged values

The baseline representation should favor correctness, debuggability, sanitizer support, and portability. Integers, floating-point numbers, booleans, null, undefined, symbols, big integers, strings, objects, and internal sentinels require non-overlapping tags and checked conversions. NaN-boxing, pointer compression, or architecture-specific immediate formats are optional later optimizations behind a representation interface.

No script-visible operation may reveal pointer bits, uninitialized padding, allocator patterns, or internal sentinels. Numeric conversions, lengths, indexes, offsets, typed-array bounds, and allocation sizes use checked arithmetic.

## Object model and property storage

Ordinary objects use shapes or hidden classes that describe prototype, property keys, attributes, slot layout, and transition identity. Inline storage handles common small objects; out-of-line storage grows under controlled policies. Mutation-heavy or highly polymorphic objects transition to dictionary mode rather than create unbounded shape graphs.

Shape identity is realm-aware and cannot be accepted across incompatible runtime instances. Prototype changes invalidate dependent caches. Accessors, proxies, module namespaces, typed arrays, arguments objects, strings, arrays, functions, bound functions, and host objects use explicit exotic operation tables.

## Strings, symbols, and big integers

Strings may use compact one-byte or wider storage, ropes, slices, or external backing only with bounded flattening and ownership rules. Interning is restricted to identifiers and other demonstrated wins; attacker-controlled unique strings cannot populate immortal tables. Substrings must not retain unexpectedly huge source buffers without accounting.

Symbols preserve realm/global-registry semantics. Big integers use bounded algorithms and allocation checks; adversarial multiplication, division, conversion, and formatting require complexity limits and cancellation.

## Arrays and indexed storage

Arrays distinguish packed, holey, sparse, typed, and exotic indexed states. Length changes, deletions, accessors, prototype indexed properties, and species behavior must invalidate optimistic paths. Capacity growth uses overflow-safe policies and semantic memory attribution.

Typed arrays and array buffers model detached, shared, resizable, growable, transferred, and out-of-bounds states explicitly. Every fast path rechecks state after callbacks or operations that may detach or resize backing memory.

## Inline caches

Inline caches begin as observable optimization metadata, not hidden semantic shortcuts. Sites progress through uninitialized, monomorphic, polymorphic, megamorphic, and disabled states. Cache keys include operation kind, shape or prototype guards, realm, indexed-element kind, and any host-policy dependency.

A cache hit executes only after all guards. Miss handlers share the same semantic operation as the interpreter. Cache state is bounded, resettable, inspectable, and excluded from authoritative serialization.

## Built-ins and intrinsics

Built-ins are initialized per realm from versioned intrinsic definitions. Fast implementations preserve observable property access, species construction, iteration, proxies, side effects, errors, and realm selection. Self-hosted code, native Rust implementations, or generated stubs are each allowed only with equivalent tests and explicit trust boundaries.

Intrinsics cannot be silently shared when mutable state, identity, compartments, locale, or policy differ. Immutable data may be shared only after proof that no realm can mutate or infer another realm.

## Memory and observability

The runtime charges value cells, shapes, transition tables, property storage, strings, symbols, code, caches, and external backing to realms and documents. DevTools can explain representation changes, shape churn, dictionary conversion, cache states, and retained external memory without making addresses or secrets visible.

## Non-negotiable invariants

- Representation optimizations never alter observable ECMAScript semantics.
- Every speculative property or indexed access has complete guards and a correct miss path.
- Shape, cache, realm, and prototype identities cannot cross incompatible boundaries.
- Attacker-controlled data cannot create unbounded immortal intern tables or cache metadata.
- Detached, resized, shared, and transferred buffer states are explicit and revalidated.

## Required evidence

- Test262 object, array, proxy, typed-array, string, symbol, BigInt, and built-in shards.
- Property-operation differential traces against the reference interpreter.
- Shape-transition, cache-state, prototype mutation, realm, and proxy fuzzing.
- Object-size and memory-retention measurements on representative application corpora.
- Benchmarks that separate lookup semantics, warm-up, polymorphism, code size, and end-to-end interaction.

## Known risks and unresolved questions

- Shape proliferation can trade CPU speed for large metadata growth.
- Fast arrays and typed arrays are frequent sources of stale-state and bounds defects.
- String ropes or slices can create latency cliffs and accidental retention.
- Self-hosted built-ins can complicate bootstrap, debugging, and security review.

## Primary sources

- ECMA-262 — https://tc39.es/ecma262/
- Test262 — https://github.com/tc39/test262
- V8 Sparkplug — https://v8.dev/blog/sparkplug
- JavaScriptCore overview — https://docs.webkit.org/Deep%20Dive/JSC/JavaScriptCore.html

## Change discipline

This document is a research and design baseline, not an implementation claim. Any accepted decision must update the owning Blueprint chapter, relevant requirements, risks, ADRs, work packages, tests, and machine-readable records in the same change.
