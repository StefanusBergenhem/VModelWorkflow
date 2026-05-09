---
purpose: Step-by-step green phase and refactor procedure with DbC discipline.
audience: vmodel-skill-implement-leaf
status: active
---

# TDD Green Phase and Refactor

**Contents.** DD parse order · Read sequence · Writing minimum code · Test loop ·
Refactor discipline · Complexity limits · Clean code rules · Cross-links.

---

## 1. DD parse order

Parse the DD completely before writing any code. Partial reads produce partial
implementations.

Read in this order — each section informs the next:

1. Front-matter: `scope`, `governing_adrs`, `version`.
2. Public Interface entries — signatures, preconditions, postconditions
   (both branches), invariants, typed errors, thread-safety category,
   side-effect declaration.
3. Data Structures — field types, invariants, nullability, immutability class.
4. Algorithms — result properties (NOT steps; see below).
5. State Machine — states, transitions, guard conditions, initial state, terminal
   states.
6. Error Handling section — error matrix (condition → typed error → caller
   obligation).

After reading, build a mental (or written) map:

```
Public Interface entries → which Data Structures they return / consume
Data Structures → which invariants must be enforced at construction / mutation
Algorithms → which Interface entries call them
State Machine → which Interface entries trigger transitions
Error matrix → which exceptions / error values the implementation must produce
```

If a contract slot is missing or ambiguous, HALT (refusal A in SKILL.md) before
starting — ambiguity discovered mid-implementation costs more than a clear
upfront block.

---

## 2. Read sequence (inputs before code)

Order matters. Do not skip steps or reorder.

```
1. detailed_design.md   — full parse (Section 1 above)
2. governing_adrs       — each ADR in DD front-matter; extract constraints
3. testspec.md          — case list only; note which contracts each case targets
4. rendered test files  — confirm file layout, assertion style, test framework
5. .vmodel/config.yaml  — commands.test, commands.lint, build.retry.*
6. Project conventions  — .vmodel/references/ + conventions.md if present
```

Do NOT read the test files for implementation guidance. Read them only to
understand framework idioms and file layout. The DD is the spec.

---

## 3. Writing minimum code

**Minimum means:** the smallest correct implementation that satisfies all DD
contracts. Not the fastest, not the most general, not the most future-proof.

**One contract at a time.** Implement interfaces in dependency order — implement
helper/private methods called by public ones first, then the public surface.

**Trust boundary stance.** The DD states whether each entry is inside a trust
boundary (DbC: callers honour preconditions) or at a trust boundary (defensive:
validate every input). Honour this stance. Do not add defensive checks to
trusted-internal paths; do not skip validation at external entry points.

**Architecture boundary.** Domain code imports no infrastructure packages (no
DB, HTTP, filesystem, framework). If the DD's contracts require I/O, the DD will
specify an interface; implement that interface in the infrastructure layer.
Functional core, imperative shell.

**Nullability.** If the DD forbids null on a parameter, enforce it at the entry
point. If the DD forbids null on a return, the implementation must not return
null — use Optional, empty collection, or Null Object as the DD specifies.

**No extra features.** If a behaviour is not in the DD, do not implement it.
User requests "while you're at it" additions are refusal F.

---

## 4. Test loop

```
while not all_tests_pass:
    run: commands.test
    for each failing test:
        identify which DD contract is not yet satisfied
        implement or fix the code to satisfy that contract
        do not modify the test to pass
```

If a test is wrong (e.g., asserts a property the DD does not specify), surface
refusal G — escalate to `vmodel-skill-render-tests`; do not weaken or delete.

If tests pass but implementation violates a DD contract the tests do not cover,
fix the implementation anyway. The DD is the spec; test coverage is not
exhaustive.

---

## 5. Refactor discipline

Tests passing is the gate to refactor, not the end of the work.

Apply these regardless of whether the first implementation was "clean enough":

**Data structure invariants.** Every invariant in the DD's Data Structures section
must be enforced at the construction site (constructor, factory method, builder
`build()`). Not as a comment. Not only in tests.

```
DD invariant: "items list is non-empty after construction"
Implementation: constructor must throw if items.isEmpty()
```

**Thread-safety category (Goetz).** Honour the category stated in each Public
Interface entry:

| Category | Implementation obligation |
|---|---|
| Immutable | All fields final; no setters; defensive copies on input/output collections |
| Thread-safe | All mutable state guarded; prefer java.util.concurrent over synchronized |
| Conditionally thread-safe | Document which compound operations require external locking |
| Thread-compatible | No internal synchronization; callers take responsibility |
| Thread-hostile | Document that the class must not be shared across threads |

**Error matrix completeness.** Every row in the DD's error matrix must have an
implementation path that produces the specified typed error. Verify with a quick
trace: for each matrix row, find the code path that throws/returns it.

**Complexity limits.** From `develop-code` precursor — enforced here:

| Metric | Target | Hard limit |
|---|---|---|
| Function length | 20 lines | 50 lines |
| Cyclomatic complexity | — | 10 per function |
| Nesting depth | — | 3 levels |
| Parameters | 3 | 5 (use parameter object above 5) |

Exceeding hard limits is a HALT condition, not a style warning. If the DD cannot
be implemented within limits, the DD needs decomposition — escalate.

**Clean code rules (lifted from `develop-code`).**

- No null returns. Use Optional, empty collection, or Null Object.
- No empty catch blocks. At minimum: log and re-throw.
- Fail-fast at boundaries: validate inputs at the public API surface.
- Error messages include context: operation + input + expected state.
- Resource cleanup mandatory: try-with-resources, defer, RAII.
- Names reveal intent; one word per concept; domain vocabulary.
- No dead code. No commented-out code. No TODO stubs for unspecified features.
- DRY, KISS, YAGNI.
- SOLID: Single Responsibility, Open/Closed, Liskov, Interface Segregation,
  Dependency Inversion.

---

## 6. Algorithm postcondition discipline

When the DD specifies an algorithm result property, implement to the property —
not to a procedure.

The DD's algorithm postconditions are *result properties*, never steps:

| Wrong (algorithmic) | Correct (result property) |
|---|---|
| "iterate the list and compare adjacent elements" | "returned list is non-descending AND is a permutation of input (multiset equality)" |
| "query DB then update cache" | "after call, cache holds entry for key matching DB row at call time" |

Both halves are required for transformation results (e.g., sort: ordered AND
permutation). Specifying only one half lets degenerate implementations pass
review.

---

## Cross-links

`fix-mode-taxonomy.md` · `contract-implementation.md` · `SKILL.md` (refusal table)
