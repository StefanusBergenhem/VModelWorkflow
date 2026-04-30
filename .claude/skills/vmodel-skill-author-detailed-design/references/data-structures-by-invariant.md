# Data structures by invariant

Specify what must be true of the data, not how the fields are laid out.

## Required parts per data structure

| Part | Required when |
|---|---|
| **Fields** (name, type, per-field invariant) | Always |
| **Structure invariants** (across-field properties) | When properties span multiple fields |
| **Ownership** (who constructs / mutates / releases) | Always |
| **Lifetime** (how long it lives, what bounds it) | Always |
| **Returned-object semantics** | When the structure crosses the public interface |

Slot-fill: `templates/data-structure-entry.yaml.tmpl`. Schema: `$defs/data_structure_entry`.

## Type vocabulary — one level above the language

| Use | Not |
|---|---|
| "non-negative integer" | `uint32_t`, `int32`, `Integer` |
| "UTC timestamp, millisecond precision" | `Instant`, `LocalDateTime` |
| "list of <T>" or "ordered sequence of <T>" | `LinkedList<T>`, `ArrayList<T>` |
| "map from K to V; K-uniqueness assumed" | `HashMap<K,V>`, `TreeMap<K,V>` |
| "byte sequence, UTF-8" | `String` |
| "money: integer minor-units + ISO-4217 currency" | `BigDecimal`, `Decimal` |

Naming a concrete language collection inside the DD → finding `anti-pattern.implementation-leaking-interface`. State the property (uniqueness, ordering, lookup-time bound), not the structure that delivers it.

When bit-width or layout is contractual (wire format, fixed-size buffer) → state it explicitly: *"32-bit unsigned big-endian"* in a packet spec is a contract.

## Invariants — when written, what they look like

Every invariant must be testable: a unit test can assert it without contrived setup.

| Slot-fill | Example |
|---|---|
| Range constraint | *"`expires_at` is strictly in the future when constructed"* |
| Cross-field constraint | *"`amount` and `currency` are both present or both absent"* |
| Foreign-key / referential | *"`worker_id` matches a row in `workers`"* |
| Multiset / aggregate | *"sum of `line.line_total` over Lines equals `subtotal`"* |
| Encoding | *"all bytes in `payload` are valid UTF-8"* |

Invariants vs preconditions: invariant lives on the data structure (true whenever observed); precondition lives on the function (true on the way in).

## Returned-object semantics — five distinct shapes

When the structure crosses the public interface, state which shape applies:

| Shape | Meaning |
|---|---|
| **Copy** | Caller receives a fresh instance; mutations isolated |
| **Live view** | Caller's reference into supplier's state; mutations observable on either side |
| **Read-only reference** | Caller cannot mutate; supplier may continue to (state if so) |
| **Read-only snapshot** | Caller observes an immutable copy taken at call time |
| **Ownership transfer** | Caller takes responsibility; supplier no longer owns |

Returning a mutable object without naming the shape → finding `check.data.returned-mutable-without-semantics`.

## Shared mutable state — always a contract

When a field is observed or mutated by more than one thread or caller, the DD states:

```yaml
field: outstanding_claims
type: <type>
invariant: <what holds whenever observed>
ownership: "Shared across worker threads"
lock: <which lock guards the field>
happens_before: <publication / lock release-acquire / atomic CAS>
readers: <who may read>
writers: <who may write>
```

Undocumented shared field → finding `anti-pattern.designing-for-races`.

## When to write a Data Structure entry

Write an entry when the structure satisfies any of:
- Has invariants beyond what the type system enforces.
- Crosses the public interface (returned or accepted).
- Is shared across threads or callers.
- Has non-obvious ownership or lifetime.

When the structure is a pure local variable / ephemeral builder with no invariants → skip it; that is implementation, not contract.

## Cross-link

`function-contracts.md` (data structures in signatures) · `state-and-concurrency.md` (concurrency story) · `anti-patterns.md` · `templates/data-structure-entry.yaml.tmpl`
