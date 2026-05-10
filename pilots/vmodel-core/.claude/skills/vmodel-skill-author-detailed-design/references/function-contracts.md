# Function contracts

Every Public Interface entry is a contract, not a signature.

## The nine contract elements

| # | Element | Required when |
|---|---|---|
| 1 | Signature (name, parameter types, return type) | Always |
| 2 | Preconditions | Always — state "none beyond callable" if so |
| 3 | Postconditions split: `on_success`, `on_failure` | Always |
| 4 | Invariants | When the function preserves a property across the call |
| 5 | Errors (typed enum) | When any failure path exists |
| 6 | Nullability per parameter and return | Always (state explicitly per language) |
| 7 | Side effects | Always — state "none" if so |
| 8 | Thread-safety category | Always (Goetz: immutable / thread-safe / conditionally-thread-safe / thread-compatible / thread-hostile) |
| 9 | Complexity notes | When time/space bound is part of the contract |

Slot-fill: `templates/public-interface-entry.yaml.tmpl`. Schema: `$defs/public_interface_entry`.

## Postconditions split — both branches mandatory

```yaml
postconditions:
  on_success:
    - <state mutation, return-value constraint, idempotency, old-value relation>
  on_failure:
    - <typed error returned + state guarantee: 'no mutation' | 'bounded to X' | 'compensated within Nms'>
```

Single-branch `postconditions:` → finding `check.contract.postcondition-failure-branch-missing`.

## Postconditions = result property, NOT steps

When stating what the function guarantees on success → describe the property of the return value or post-state. Do **not** describe the steps the implementation takes.

| Algorithmic (refuse — refusal C) | Result-property (correct) |
|---|---|
| "Shall iterate the list and compare adjacent elements" | "The returned list is non-descending under the natural ordering AND is a permutation of the input (multiset equality)" |
| "Shall query the DB then update the cache" | "After the call, the cache holds an entry for the queried key whose value matches the DB row at call time" |

**Two halves rule.** Transformation results require both halves of the property — *ordered* AND *permutation*. Specifying only one half lets degenerate implementations pass. See `algorithms.md`.

## Liskov substitution (when subtypes exist)

When the function has subtypes / variant implementations:
- Preconditions may only weaken in subtypes.
- Postconditions may only strengthen.
- Invariants must be preserved.

Violation → finding `check.contract.liskov-violation`. Surface; do not paper over.

## Units of measure are contract

When a parameter or return is numeric, do one of:

| Pattern | Example |
|---|---|
| Type carries the unit | `Metres altitude`, `Millis timeout`, `BasisPoints rate` |
| Contract names the unit and range | *"`altitude`: metres above mean sea level; valid [-500, 12000]"* |

Bare `double altitude` with no unit → finding `anti-pattern.implicit-unit`.

## Defensive vs DbC — pick one per trust boundary

When inside a trust boundary → DbC: callers honour preconditions; no defensive checks.

When at a trust boundary (external I/O, IPC, untrusted process edge) → defensive: validate every input.

State the stance in the contract: *"Caller-validated input; no defensive checks inside the trust boundary."*

## Nullability — explicit per slot

When `null` is permitted on input → state what it means (absent / default).

When `null` is permitted on return → state what it means (no result / not found).

When `null` is forbidden → state that explicitly (precondition on input, invariant on return).

Languages with `Optional<T>` / `Maybe a` / `T?` carry the meaning in the type; the contract still states what `None` means in domain terms.

## Complexity — only when contractual

State complexity notes only when:
- A latency budget is allocated to this leaf by the parent Architecture
- A worst-case bound is part of correctness (real-time response, adversary-supplied input)
- An unbounded-loop / unbounded-memory pattern would be catastrophic

Form: O-notation + the input dimension. *"O(log n) in the number of active claims under the connection-pool ceiling."*

## Cross-link

`algorithms.md` (postcondition discipline) · `state-and-concurrency.md` (thread-safety) · `data-structures-by-invariant.md` (returned-object semantics) · `anti-patterns.md` (catalog) · `templates/public-interface-entry.yaml.tmpl`
