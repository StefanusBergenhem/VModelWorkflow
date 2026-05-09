# Language idioms for test rendering

Per-language conventions for test file structure, naming, assertions, test doubles,
and VERIFIES comment syntax. Other languages extend by analogy.

## Table of contents

- [Go](#go)
- [Python](#python)
- [Java / JUnit 5](#java--junit-5)
- [TypeScript / Vitest](#typescript--vitest)
- [Language detection](#language-detection)

---

## Go

**Framework:** `testing` standard library + `testify` (`github.com/stretchr/testify`).

**File grouping:** one `_test.go` file per package. All cases for a scope land in
`<scope>_test.go`. Integration tests follow the same pattern in the component package.

**Naming:** `Test<CaseTitlePascal>(t *testing.T)`. CaseTitlePascal = case `title:`
converted to PascalCase with spaces/hyphens removed.

**VERIFIES comment:** immediately above the `func Test...` line.
```go
// VERIFIES: TC-expiry-001 → DD-expiry-calc.expiry_logic.idle_timeout
func TestReturnsEarliestOfIdleAndAbsolute(t *testing.T) {
```

**Parameterized (table-driven):**
```go
// VERIFIES: TC-expiry-002, TC-expiry-003 → DD-expiry-calc.expiry_logic.boundary
func TestBoundaryValues(t *testing.T) {
    tests := []struct {
        name     string
        input    int64
        expected int64
    }{
        {"at_zero", 0, 0},
        {"at_max", 9223372036854775807, 9223372036854775807},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := calc.Compute(tt.input)
            assert.Equal(t, tt.expected, result)
        })
    }
}
```

**Test doubles:** use interface-based fakes or `testify/mock`. Declare the fake inline
in the test file or in a `testdata/` subdirectory — never in production code.

**Error assertions:**
```go
_, err := unit.SetRate(-1)
require.Error(t, err)
assert.Contains(t, err.Error(), "must be positive")
```

**Red phase verification:** `go test ./... -run TestName` should fail with a compilation
error (if not implemented) or a test failure (if the method exists but returns wrong value).
If the method does not exist yet, the package will not compile — that is the expected red
state for Go.

---

## Python

**Framework:** `pytest`. Assertions use plain `assert` with `pytest`'s rewriting for
helpful failure messages.

**File grouping:** one `test_<scope_slug>.py` file per scope. Integration tests land in
`tests/integration/test_<scope_slug>.py`. System tests in `tests/system/test_<scope_slug>.py`.

**Naming:** `test_<case_title_slug>`. Title slug = case `title:` lowercased, spaces
replaced with underscores, non-alphanumeric removed.

**VERIFIES comment:** immediately above the `def test_...` line.
```python
# VERIFIES: TC-expiry-001 → DD-expiry-calc.expiry_logic.idle_timeout
def test_returns_earliest_of_idle_and_absolute():
```

**Class grouping (optional):** group related cases in a `class Test<SuiteName>` when the
TestSpec uses `suite:` groupings.

**Parameterized:**
```python
# VERIFIES: TC-expiry-002, TC-expiry-003 → DD-expiry-calc.expiry_logic.boundary
@pytest.mark.parametrize("input_val,expected", [
    (0, 0),
    (9223372036854775807, 9223372036854775807),
], ids=["at_zero", "at_max"])
def test_boundary_values(input_val, expected):
    result = calc.compute(input_val)
    assert result == expected
```

**Test doubles:** `unittest.mock.MagicMock` or simple hand-written fakes. Prefer fakes
for collaborators with defined contracts. Mock only infrastructure at the boundary.

**Error assertions:**
```python
with pytest.raises(ValueError, match="must be positive"):
    unit.set_rate(-1)
```

**Fixture setup (pytest):** use `@pytest.fixture` for shared setup. Keep fixtures
minimal — only what every test in the file requires. Per-test setup goes inline.

**Red phase verification:** `pytest --collect-only` must succeed (file is parseable).
`pytest` must show FAILED for every rendered case (no implementation yet).

---

## Java / JUnit 5

**Framework:** JUnit 5 (`org.junit.jupiter`). Assertions: `org.junit.jupiter.api.Assertions`
+ AssertJ (`org.assertj.core.api.Assertions`) for fluent assertions.

**File grouping:** one `<ScopeNamePascal>Test.java` class per scope. Integration tests use
the same class with `@Tag("integration")`. System tests use `@Tag("system")`.
Nested `@Nested` classes group by TestSpec `suite:` field.

**Naming:** `void test<CaseTitlePascal>()`. Test class annotated `@DisplayName("<scope>")`.
Method annotated `@DisplayName("<case title>")`.

**VERIFIES comment:** immediately above the `@Test` / `@ParameterizedTest` annotation.
```java
// VERIFIES: TC-expiry-001 → DD-expiry-calc.expiry_logic.idle_timeout
@Test
@DisplayName("returns earliest of idle and absolute thresholds")
void testReturnsEarliestOfIdleAndAbsolute() {
```

**Arrange / Act / Assert:** three comment sections, visually separated by blank line.
```java
// Arrange
var inputs = ExpiryInputs.of(idleTimeout, absoluteTimeout);

// Act
var result = calculator.compute(inputs);

// Assert
assertEquals(1735689600L, result.epochSecond());
```

**Parameterized:**
```java
// VERIFIES: TC-expiry-002, TC-expiry-003 → DD-expiry-calc.expiry_logic.boundary
@ParameterizedTest(name = "{0}")
@MethodSource("boundaryValues")
@DisplayName("boundary values")
void testBoundaryValues(String name, long input, long expected) {
    assertEquals(expected, calculator.compute(input));
}

static Stream<Arguments> boundaryValues() {
    return Stream.of(
        Arguments.of("at_zero", 0L, 0L),
        Arguments.of("at_max", Long.MAX_VALUE, Long.MAX_VALUE)
    );
}
```

**Test doubles:** Mockito (`org.mockito.Mockito`) for mocks and spies. Use
`@ExtendWith(MockitoExtension.class)`. Prefer real fakes for collaborators with
defined contracts.

**Error assertions (JUnit 5):**
```java
var ex = assertThrows(IllegalArgumentException.class, () -> unit.setRate(-1));
assertThat(ex.getMessage()).contains("must be positive");
```

**Red phase verification:** `./gradlew test` (or `mvn test`) should fail compilation if
the class does not exist, or show test failures if the class exists but the method is
not implemented.

---

## TypeScript / Vitest

**Framework:** Vitest. Import: `import { describe, it, expect, vi } from 'vitest'`.

**File grouping:** one `<scope>.test.ts` file per scope. Integration tests follow the
same pattern. System tests in `tests/system/<scope>.test.ts`.

**Naming:** `it('<case title>')` inside a `describe('<scope>')` block. Title is the
exact `title:` value from the TestSpec (no transformation).

**VERIFIES comment:** immediately above the `it(...)` call.
```typescript
// VERIFIES: TC-expiry-001 → DD-expiry-calc.expiry_logic.idle_timeout
it('returns earliest of idle and absolute thresholds', () => {
```

**Parameterized:**
```typescript
// VERIFIES: TC-expiry-002, TC-expiry-003 → DD-expiry-calc.expiry_logic.boundary
it.each([
  { name: 'at_zero', input: 0n, expected: 0n },
  { name: 'at_max', input: BigInt('9223372036854775807'), expected: BigInt('9223372036854775807') },
])('boundary values — $name', ({ input, expected }) => {
  expect(calculator.compute(input)).toBe(expected)
})
```

**Arrange / Act / Assert:** three comment sections.
```typescript
// Arrange
const inputs = { idleTimeout: 300, absoluteTimeout: 1735689600 }

// Act
const result = calculator.compute(inputs)

// Assert
expect(result).toBe(1735689600)
```

**Test doubles:** `vi.fn()` for mocks, `vi.spyOn()` for spies. For fakes, write a
plain object implementing the interface. Prefer fakes over mocks.

**Error assertions:**
```typescript
expect(() => unit.setRate(-1)).toThrow('must be positive')
```

**Red phase verification:** `npx vitest run` should fail (tests fail or the import cannot
be resolved). The test file must be parseable (no syntax errors).

---

## Language detection

When `.vmodel/config.yaml` contains a `language:` field, use that. When absent, infer
from `commands.test_unit`:

| Substring in `commands.test_unit` | Language |
|---|---|
| `go test` | Go |
| `pytest` or `python -m pytest` | Python |
| `gradle test` or `mvn test` or `mvn surefire` | Java |
| `vitest` or `jest` | TypeScript |

If detection is ambiguous, ask before rendering.

For languages not listed (Rust, C++, Kotlin, Swift, etc.), apply the same structural
principles — VERIFIES comment, Arrange/Act/Assert, hardcoded oracle values, test doubles
at infrastructure boundaries — using the project's established test framework idioms.
