---
name: derive-test-cases
description: >
  Derive comprehensive test cases from a design document using V-model test derivation strategies:
  requirement-based testing, equivalence class partitioning, boundary value analysis, and fault
  injection. Use this skill when the user asks to write tests, derive test cases, create a test
  suite, or implement TDD red phase for a module that has a design. Also use when the user says
  "derive tests", "write tests for this design", "what should I test", or mentions test derivation,
  test coverage planning, or wants to go from design to tests.
user-invocable: true
---

# Derive Test Cases

Derive test cases from a design document. The goal: every behavior, interface boundary, and error
condition has at least one test that would **fail if the implementation were deleted**.

## Input

A **design document** describing the unit to test. This can be any format — markdown, YAML, plain
text, structured tables, or informal descriptions. Look for these testable elements:

- **Interfaces** — inputs with types, constraints, ranges; outputs with expected shapes
- **Behavior rules** — conditions and their expected results
- **Error handling** — what happens on invalid input, failures, edge conditions
- **Configuration** — defaults, limits, tuneable parameters
- **Internal state** — state that persists across calls, affecting behavior
- **Dependencies** — external components this unit relies on (clock, storage, network)

If the design lacks any of these, work with what's there. If it's too vague to derive meaningful
tests, HALT and ask the user for clarification.

## Principles

These guide every decision. When in doubt, come back to these.

- **Spec-to-test, never code-to-test.** Derive tests from the design document only. Never read or
  mirror implementation logic. Hardcode expected values from the spec, not computed from code.
- **Test behavior, not implementation.** Verify observable outputs given specific inputs. Do not
  test internal method call sequences, data structures, or algorithm choices.
- **Assert specific expected values.** Every test must assert an exact output value derived from
  the design. `assertNotNull`, `assertTrue(x)`, or "does not throw" as the sole assertion is
  worthless — it passes for any implementation.
- **Mock only at infrastructure boundaries.** Use real implementations for domain collaborators.
  Mock or stub only infrastructure dependencies (clock, database, HTTP, filesystem).
  Preference: real > fake > stub > mock. If mocking > 2 dependencies, the design may need
  revisiting — HALT.
- **State verification over behavior verification.** Check outcomes (what state is the system in),
  not interactions (what calls were made). Use `verify()` only when the interaction IS the
  observable behavior (e.g., "notification was sent").
- **Arrange / Act / Assert.** Three visually separated sections in every test. Act calls the unit
  under test exactly once.
- **Parameterize where natural.** When multiple tests differ only in input/expected output (common
  for equivalence classes and boundary values), use parameterized tests to eliminate duplication.
- **F.I.R.S.T.** Tests are Fast, Independent, Repeatable, Self-validating, Timely. Inject clocks
  and random seeds. No shared mutable state between tests. No real I/O.

## What to do

Apply four derivation strategies to build a **coverage matrix** mapping every design element to
at least one test case. Read `references/derivation-strategies.md` for details on each strategy.

1. **Requirement-based** — one test per behavior rule or condition
2. **Equivalence class partitioning** — partition each input by type/constraints, test one per class
3. **Boundary value analysis** — test at min, max, just-below, just-above for constrained values
4. **Error handling / fault injection** — one test per error condition, plus implicit faults

Then write the tests. Check every test against `references/testing-anti-patterns.md` and
`references/ai-testing-failures.md` before delivering.

## Output

1. **Test source file(s)** — real, compilable test code in the requested language/framework.
   Test names describe the scenario (input condition + expected outcome), not just the method name.

2. **Coverage matrix** — a table mapping every design element to test case(s) and derivation
   strategy. Every design element must appear. Format:

   ```
   | Design Element            | Test Case(s)                     | Strategy    |
   |---------------------------|----------------------------------|-------------|
   | behavior: startup limit   | test_startup_limits_rate_to_min  | req-based   |
   | error: negative rate      | test_negative_rate_raises        | error       |
   | input: rate [0, MAX]      | test_rate_at_zero, _at_max       | boundary    |
   ```

## Self-check

Before delivering, verify:

1. **Delete test:** Would every test fail if I deleted the implementation?
2. **Wrong answer:** Would every test catch a wrong but structurally valid answer?
3. **Assertion audit:** Does every test assert a specific expected value (not just not-null)?
4. **Mock audit:** Can I explain each test double in one sentence? Is any domain object mocked?
5. **Coverage completeness:** Does the coverage matrix cover every design element?
6. **Error ratio:** Count error-path tests vs happy-path tests. If ratio < 1:2, missing cases.

## HALT conditions

Stop and ask the user if:
- The design is too vague to derive specific expected values
- A behavior rule is ambiguous about expected output
- You need to mock something but the design doesn't describe the dependency's contract
- You're mocking more than 2 dependencies — the design may have a coupling problem
- You're unsure which language or test framework to use
