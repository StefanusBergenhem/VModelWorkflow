# Test Derivation Strategies

Four strategies for deriving test cases from a design. Apply all four to every unit.

---

## Strategy 1: Requirement-Based Testing

**Source:** Behavior rules, conditions, expected results — however the design expresses them.

One test per behavior rule or condition. For compound conditions (A AND B), test each condition's
influence independently. For sequential steps, test the happy path and each step's failure path.

This is the universal baseline — every V-model standard requires it.

---

## Strategy 2: Equivalence Class Partitioning

**Source:** Inputs with types, constraints, and ranges.

Divide each input into groups where the unit behaves identically. Test one representative per group.

| Input characteristic | Classes to derive |
|---|---|
| Enum with defined values | One class per value |
| Numeric with min/max | Valid range, below range, above range |
| String | Empty, typical, at max length (if constrained) |
| Boolean | true, false |
| Collection | Empty, single element, multiple elements |
| Object/struct | Valid complete, missing optional fields, missing required fields |

Also derive invalid classes: null/missing, wrong type, out of range.

When a unit has multiple inputs, test each input's classes independently while holding others at
valid defaults. Only combine inputs that the design says interact (behavior rules referencing
multiple inputs).

---

## Strategy 3: Boundary Value Analysis

**Source:** Any constrained value — numeric ranges, string lengths, collection sizes, config limits.

For a value with constraint `>= min` and `<= max`:

| Test point | Value | Expected |
|---|---|---|
| Below minimum | min - 1 (or min - epsilon) | Error / rejection |
| At minimum | min | Valid behavior |
| Just above minimum | min + 1 | Valid behavior |
| Just below maximum | max - 1 | Valid behavior |
| At maximum | max | Valid behavior |
| Above maximum | max + 1 (or max + epsilon) | Error / rejection |

Apply the same logic to string lengths, collection sizes, and configuration parameters.

---

## Strategy 4: Error Handling and Fault Injection

**Source:** Explicit error conditions in the design, plus implicit faults.

One test per explicit error condition. Then probe for implicit failures the design may not
have listed:

| Fault category | What to test |
|---|---|
| Null/missing inputs | Pass null/nil/None for each input |
| Resource exhaustion | Empty collections, zero-length strings, maximum-size inputs |
| Dependency failures | If the design implies external calls, what if they fail/timeout? |
| Concurrent access | If the design mentions thread-safety, test concurrent calls |
| State corruption | If internal state exists, call methods in unexpected order |

---

## Combining Strategies: The Coverage Matrix

After applying all four strategies, build a coverage matrix mapping every design element to its
test case(s). This is a mandatory output — it proves completeness and provides traceability.

| Design Element            | Test Case(s)                     | Strategy    |
|---------------------------|----------------------------------|-------------|
| behavior: startup limit   | test_startup_limits_rate_to_min  | req-based   |
| error: negative rate      | test_negative_rate_raises        | error       |
| input: rate [0, MAX]      | test_rate_at_zero, _at_max       | boundary    |
| input: rate [0, MAX]      | test_rate_mid_range              | equivalence |

Walk the matrix after writing all tests: every behavior rule tested? Every error condition?
Every input covered by at least equivalence class + boundary tests? Stateful transitions?
Configuration variants? Any row without a test is a gap.

---

## Parameterized Tests

When multiple tests differ only in input and expected output — common for equivalence classes
and boundary values — use parameterized tests to eliminate duplication:

- **Python pytest:** `@pytest.mark.parametrize("input,expected", [...])`
- **Java JUnit 5:** `@ParameterizedTest` with `@CsvSource` or `@MethodSource`
- **Go testing:** table-driven tests with `for _, tc := range cases { t.Run(tc.name, ...) }`

Use parameterized tests for data variations. Use separate named tests when the assertion logic
differs between cases.

