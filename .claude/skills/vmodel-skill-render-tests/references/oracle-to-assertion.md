# Oracle-to-assertion translation

Maps each oracle form in a TestSpec `expected:` field to the corresponding assertion
pattern. Read in full before Step 3 (translate each case to test code).

## Table of contents

- [Oracle form taxonomy](#oracle-form-taxonomy)
- [Specific value](#specific-value)
- [Bounded predicate](#bounded-predicate)
- [Property / invariant](#property--invariant)
- [Enumerated set or collection](#enumerated-set-or-collection)
- [Error / exception](#error--exception)
- [Side effect](#side-effect)
- [Timing bound](#timing-bound)
- [Weak oracle — HALT](#weak-oracle--halt)

---

## Oracle form taxonomy

TestSpec `expected:` values fall into six well-defined forms. Each form has a direct
translation. If a value does not fit any form, it is a weak oracle — halt.

| Form | Example in TestSpec | Translation |
|---|---|---|
| Specific value | `1735689600` | Equality assertion |
| Bounded predicate | `"result <= 50ms"` | Comparison assertion |
| Property / invariant | `"result is permutation of input AND non-descending"` | Property check |
| Enumerated set | `["PENDING", "ACTIVE"]` | Membership assertion |
| Error / exception | `"raises ValueError: rate must be >= 0"` | Exception assertion |
| Side effect | `"email sent to user@example.com within 60s"` | Side-effect assertion (spy/mock) |
| Timing bound | `"total elapsed <= 5 minutes p95"` | Elapsed-time assertion |

---

## Specific value

The oracle names one exact output.

```
expected: 1735689600
expected: { result: 1735689600, branch_taken: "idle" }
expected: "REJECTED"
```

**Translation:** equality assertion on the exact value.

```java
// Java
assertEquals(1735689600L, result);
assertEquals("REJECTED", result.status());

// Python
assert result == 1735689600
assert result == {"result": 1735689600, "branch_taken": "idle"}

// Go
assert.Equal(t, int64(1735689600), result)

// TypeScript
expect(result).toEqual(1735689600)
```

Never recompute the expected value using the same formula as the implementation
(Mirror Test anti-pattern — `unit-test.html` §3.5 *Common Anti-Patterns*).
Hardcode the value from the TestSpec.

---

## Bounded predicate

The oracle names a range or inequality constraint. Use when the spec cannot
or does not fix a single value but guarantees a bound.

```
expected: "result <= 50ms"
expected: "0 < result < MAX_RATE"
expected: "result >= 0 AND result <= 100"
```

**Translation:** comparison assertion using the exact bound.

```java
// Java
assertTrue(result.toMillis() <= 50, "expected <= 50ms, got " + result.toMillis());

// Python
assert result <= 0.050, f"expected <= 50ms, got {result}"

// Go
assert.LessOrEqual(t, result.Milliseconds(), int64(50))

// TypeScript
expect(result).toBeLessThanOrEqual(50)
```

For a two-sided bound (`0 < result < MAX_RATE`), assert both ends separately.

---

## Property / invariant

The oracle states a relationship that must hold for any valid output rather than a
single value. Common for sort, shuffle, encode/decode round-trips.

```
expected: "result is permutation of input AND non-descending"
expected: "decode(encode(input)) == input"
```

**Translation:** property check or invariant assertion.

```java
// Java — permutation + sorted
List<Integer> sorted = new ArrayList<>(input);
Collections.sort(sorted);
assertEquals(sorted, result);  // sorted is the expected canonical form

// Python — round-trip
assert decode(encode(input)) == input
```

For data-structure invariants (heap property, tree balance), assert the structural
property directly on the result. Do not call the implementation's internal methods —
query the public interface only.

---

## Enumerated set or collection

The oracle names a fixed set of acceptable values, or an exact collection.

```
expected: ["PENDING", "ACTIVE"]          # one of these two
expected: { items: [3, 7, 12], count: 3 } # exact collection
```

**Translation:** membership assertion or collection equality.

```java
// Java — membership
assertThat(result, isOneOf("PENDING", "ACTIVE"));

// Java — exact collection (order-insensitive)
assertThat(result.items(), containsInAnyOrder(3, 7, 12));

// Python — membership
assert result in {"PENDING", "ACTIVE"}

// Python — exact list (order matters)
assert result == [3, 7, 12]
```

When the TestSpec does not specify order, assert order-insensitive membership.
When the TestSpec specifies order ("items in insertion order"), assert ordered equality.

---

## Error / exception

The oracle specifies that the unit should raise / throw a specific error type and
optionally a message substring.

```
expected: "raises ValueError: rate must be >= 0"
expected: "raises IllegalArgumentException with message containing 'must be positive'"
```

**Translation:** exception assertion. Always assert on both the type and (when specified)
the message. Asserting only that something is thrown is the assertion-free anti-pattern.

```java
// Java / JUnit 5
var ex = assertThrows(IllegalArgumentException.class, () -> unit.setRate(-1));
assertThat(ex.getMessage(), containsString("must be positive"));

// Python / pytest
with pytest.raises(ValueError, match="rate must be >= 0"):
    unit.set_rate(-1)

// Go
_, err := unit.SetRate(-1)
require.Error(t, err)
assert.Contains(t, err.Error(), "must be positive")

// TypeScript / Vitest
expect(() => unit.setRate(-1)).toThrow("must be positive")
```

---

## Side effect

The oracle specifies that the unit must produce an observable side effect: an event
emitted, a notification sent, a record written.

```
expected: "email sent to user@example.com within 60s"
expected: "AuditEvent(action='LOGIN', userId=42) emitted on event bus"
```

**Translation:** use a spy or mock on the collaborator that produces the side effect.
Assert the interaction only when the interaction itself is the observable behaviour
(state-verification preference still applies when state is observable).

```java
// Java — mock for email
verify(emailSender, timeout(60_000)).send(
    argThat(msg -> msg.getTo().equals("user@example.com"))
);

// Python — spy on event bus
event_bus.emit.assert_called_once_with(AuditEvent(action="LOGIN", user_id=42))
```

Prefer asserting observable state over interaction. Use mock verification only when
no state is observable (e.g., the unit's only effect is a notification).

For timing bounds on side effects (`within 60s`), use a timeout-aware assertion or
poll with a maximum wait. Hard-sleep is the erratic-test anti-pattern — never use it.

---

## Timing bound

The oracle specifies an elapsed-time or latency percentile bound.

```
expected: "total elapsed <= 5 minutes p95"
expected: "response time < 200ms"
```

**Translation:** capture wall-clock time before and after the action; assert the delta.

```java
// Java
var start = Instant.now();
// Act
var result = unit.process(input);
var elapsed = Duration.between(start, Instant.now());
assertTrue(elapsed.toMillis() < 200, "expected < 200ms, got " + elapsed.toMillis());
```

For p95 bounds: if the test framework has no built-in percentile support, run the
action N times, sort the durations, and assert the 95th percentile value. N >= 20 is
the minimum for meaningful p95. Note this in the test as a known approximation.

---

## Weak oracle — HALT

The following patterns in `expected:` are weak oracles. They do not translate to a
meaningful assertion. HALT with the case ID and reason before rendering any test code
for that case.

| Pattern | Why it is weak |
|---|---|
| `"verifies behaviour"` | No concrete assertion possible |
| `"does not throw"` | Assertion-free — passes for any implementation |
| `"non-null"` or `"non-empty"` alone | Tautological — passes for any non-trivial implementation |
| `"instance of X"` alone | Structural-only — passes for any X subtype regardless of content |
| `"returns successfully"` | Same as assertion-free |

Report: "HALT: case `<id>` has weak oracle (`<expected value>`). Revise the TestSpec to
provide a specific value, bounded predicate, or named exception before rendering."
