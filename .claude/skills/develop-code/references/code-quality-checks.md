# Code Quality Checks

Run through this checklist for every piece of code before delivering. Each item is a concrete,
verifiable check — not a vague aspiration.

---

## Functions

- [ ] Under 50 lines (target: under 20)
- [ ] Cyclomatic complexity under 10
- [ ] Nesting depth under 4
- [ ] 3 or fewer parameters (use parameter object if more)
- [ ] Does one thing — describable without "and"
- [ ] No boolean flag parameters (split into two functions)
- [ ] No side effects in functions that return values (command-query separation)
- [ ] Return early with guard clauses to reduce nesting

## Error Handling

- [ ] No null returns — use Optional, empty collection, or Null Object
- [ ] No empty catch blocks — at minimum log and re-throw
- [ ] No null parameters accepted — validate at boundary
- [ ] Error messages include: operation attempted, input that caused error, expected state
- [ ] Resources cleaned up in finally / try-with-resources / defer / RAII
- [ ] Fail-fast: invalid inputs rejected at public API surface

## Naming

- [ ] Names reveal intent — no abbreviations unless universal (id, url, http)
- [ ] Classes are nouns, methods are verbs
- [ ] Consistent vocabulary — one word per concept across codebase
- [ ] Domain vocabulary used where appropriate
- [ ] No encodings or prefixes (no Hungarian notation, no m_ prefixes)

## Classes and Modules

- [ ] Single responsibility — one reason to change
- [ ] High cohesion — all methods use most fields
- [ ] Composition over inheritance (unless genuine "is-a")
- [ ] No god classes — if the name is "Manager", "Processor", "Handler", "Utility", reconsider

## Architecture

- [ ] Domain code has zero infrastructure imports (no DB, HTTP, filesystem, framework)
- [ ] Dependencies point inward (infrastructure depends on domain, not reverse)
- [ ] External dependencies accessed through interfaces defined by domain
- [ ] No circular package/module dependencies
- [ ] New code follows existing codebase patterns and conventions

## Dead Code

- [ ] No unreachable code paths
- [ ] No unused functions, methods, or variables
- [ ] No commented-out code
- [ ] No TODO stubs for unspecified features
- [ ] Every function traces to a design element

## Design Compliance

- [ ] Every code unit maps to a specific design element
- [ ] No functionality beyond what the design specifies
- [ ] Algorithms match the design specification
- [ ] Interface signatures match the design (types, parameters, return types)
- [ ] Error handling follows the design's error strategy

## Comments

- [ ] No comments that restate what the code does
- [ ] "Why" comments where the reason isn't obvious from context
- [ ] Public API has doc comments (Javadoc/docstring) if library code
- [ ] No commented-out code (VCS remembers)

## Immutability and State

- [ ] Fields final/const/readonly where possible
- [ ] Value objects are immutable (records, frozen dataclasses)
- [ ] Collections returned as unmodifiable views
- [ ] Mutable state is minimal and localized
- [ ] Thread-safety addressed if design requires concurrency
