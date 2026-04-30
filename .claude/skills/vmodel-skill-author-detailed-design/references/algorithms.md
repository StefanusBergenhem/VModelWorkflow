# Algorithms

Specify the result. Select the algorithm only when the algorithm is contractual.

## The two failure modes

```text
TOO VAGUE — Rule 2 fails
  "The function sorts the input list."
```

```text
CODE PARAPHRASE — Rule 1 fails (refusal C)
  "Declare a result list, iterate from 0 to length-1, compare elements,
   swap when out of order, return the result."
```

```text
RIGHT LEVEL — both rules pass
  "Returns a list containing exactly the elements of the input
   (multiset equality), in non-descending order according to the
   natural ordering. Equal elements preserve their relative order
   (stability required — downstream uses input order as tiebreaker).
   Performance: O(n log n) worst case (request-latency budget).
   Null inputs raise IllegalArgumentException."
```

## When the algorithm choice is the implementer's

Default. Specify the result property; do not specify steps.

| Bad — algorithmic postcondition | Good — result-property postcondition |
|---|---|
| "Shall iterate and compare adjacent" | "Returned list is ordered AND a permutation of the input" |
| "Shall accumulate from the first element" | "Returned value equals the sum of the multiset under <op>" |
| "Shall query DB then update cache" | "After call, cache holds an entry whose value matches the DB row at call time" |

**Two halves rule.** Transformation results need both:

- Sort: *ordered* AND *permutation* (without permutation, `return []` passes).
- Filter: *all returned satisfy the predicate* AND *no input that satisfies the predicate is dropped*.
- Map: *each output position corresponds to the same input position* AND *each output is f(input)*.

Omitting either half → finding `anti-pattern.permutation-half-omitted`.

## When the algorithm IS contractual

State it explicitly AND state why. Triggers:

| Trigger | Example |
|---|---|
| **Determinism** | *"SHA-256 (FIPS 180-4) — clients depend on bit-for-bit equivalence."* |
| **Worst-case bound** | *"Quickselect with median-of-medians pivot — O(n) worst-case required (adversary input)."* |
| **Operational constraint** | *"Reservoir sampling (Vitter 1985) — single-pass over an unrewindable stream."* |
| **Wire compatibility** | *"CRC-32 IEEE 802.3 polynomial — clients consume as stable identifier."* |

Cite a spec or paper when one applies. *"Use the standard one"* is not a contract.

## Specification-pattern selection

| Behaviour shape | Form |
|---|---|
| Pure function, transformation | Pre/postcondition + result property |
| Rule-based (N booleans → outcome) | Decision table — `templates/decision-table.md.tmpl` |
| Mode-dependent, event-driven | State machine — `state-and-concurrency.md` |
| Multi-step ordered protocol | Numbered sequence + per-step invariant |
| Complex input partitioning | Tabular spec (input partitions × output classes) |

A function may use more than one form when behaviour genuinely has both shapes.

## Decision tables — when to use

When the function's behaviour is N inputs (boolean or small-cardinality) → 1-of-M outcomes, write a table. Coverage is mechanically checkable: the rule masks must partition the 2^N (or product) input space.

Slot-fill: `templates/decision-table.md.tmpl`. The TestSpec derives one test per rule.

## Pseudocode — when it earns its keep

Write pseudocode when:
- The algorithm is contractual (above) AND prose loses precision
- A multi-step state mutation has an order that is part of the contract
- A non-obvious invariant across steps is opaque in prose

Do **not** write pseudocode when the behaviour can be expressed as a result property, when the algorithm is implementer's choice, or when the "pseudocode" would be the implementation in another notation (refusal C).

When pseudocode earns its keep → write it at one level above the implementation: data flow, conditional structure, invariants — not language syntax.

## Numbered-sequence form for protocols

When the behaviour is a multi-step interaction (handshake, two-phase commit, saga) → describe as numbered steps with the invariant that holds between steps. The TestSpec derives one robustness test per "what if step N fails".

## Cross-link

`function-contracts.md` (postcondition discipline) · `state-and-concurrency.md` · `error-handling.md` · `anti-patterns.md`
