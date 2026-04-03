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

If the design lacks any of these, work with what's there. If it's too vague to derive meaningful
tests, HALT and ask the user for clarification.

## What to do

Apply four derivation strategies to build a **coverage matrix** mapping every design element to
at least one test case. Read `references/derivation-strategies.md` for details on each strategy.

1. **Requirement-based** — one test per behavior rule or condition
2. **Equivalence class partitioning** — partition each input by type/constraints, test one per class
3. **Boundary value analysis** — test at min, max, just-below, just-above for constrained values
4. **Error handling / fault injection** — one test per error condition, plus implicit faults

Then write the tests. Check every test against `references/testing-anti-patterns.md` before
delivering.

## Output

1. **Test source file(s)** — real, compilable test code in the requested language/framework

## HALT conditions

Stop and ask the user if:
- The design is too vague to derive specific expected values
- A behavior rule is ambiguous about expected output
- You need to mock something but the design doesn't describe the dependency's contract
- You're unsure which language or test framework to use
