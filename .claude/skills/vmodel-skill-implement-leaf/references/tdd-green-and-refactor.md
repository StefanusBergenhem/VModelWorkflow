---
purpose: Step-by-step green phase and refactor procedure with DbC discipline.
audience: vmodel-skill-implement-leaf
status: active
---

# TDD Green Phase and Refactor

**Contents.** DD parse order · Read sequence · Writing minimum code · Test loop ·
Refactor discipline · Complexity limits · Clean code rules · Algorithm
postcondition discipline · AI-specific risks · Cross-links.

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

**Complexity limits.** Aligned with the craft guide (`source-code.html` §3.1
*Complexity Constraints* and §3.2 *Function Design*):

| Metric | Target | Hard limit |
|---|---|---|
| Function length | 5–15 lines | 50 lines |
| File length | — | 500 lines |
| Cyclomatic complexity | — | 10 per function |
| Nesting depth | — | 3 levels |
| Parameters | 0–3 | 5 (use parameter object above 5) |

Exceeding hard limits is a HALT condition, not a style warning. If the DD cannot
be implemented within limits, the DD needs decomposition — escalate.

**Clean code rules.**

- No null returns where DD forbids null. Use Optional, empty collection, or Null
  Object.
- No empty catch blocks. At minimum: log and re-throw or convert to typed error.
- Fail-fast at boundaries: validate inputs at the public API surface (the
  defensive stance, when the DD says so).
- Error messages include context: operation + input + expected state.
- Resource cleanup mandatory: try-with-resources, defer, RAII.
- Names reveal intent; one word per concept; domain vocabulary from the project
  glossary.
- No magic numbers. When a numeric or string literal carries domain meaning,
  extract a named constant.
- Beware primitive obsession. When a primitive (`String`, `int`, `double`)
  carries a domain concept (email, temperature, money), a value object is the
  right shape — but only if the DD specifies one. Implementing inside the DD's
  chosen types is the rule; raise an issue against the DD if a primitive is
  load-bearing for a domain concept.
- Comments explain *why*, not *what*. If a comment paraphrases the code, delete
  the comment and improve the names. Public-API doc comments stating contracts
  (preconditions, postconditions, exceptions) are exempt.
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

## 7. AI-specific risks

The implementer is an LLM. The craft guide (`source-code.html` §3.4
*AI-Assisted Development*) catalogues the LLM failure modes that pass tests
but fail in production. Apply these guards at refactor time, not only at
review time.

**When generating a call to an external library:** verify that the method
name, signature, and return type exist in the actual library version pinned
in the project. Plausible-but-fictional methods (correct package, wrong
method) are the most common LLM correctness failure. Tooling: read the
library's published API docs or local sources; do not trust training-data
recall.

**When using a configuration framework:** verify each property name against
the framework's actual configuration schema. Hallucinated config keys
compile and run silently broken — the framework treats unknown keys as
no-ops.

**When code computes a range or boundary:** explicitly reason about
inclusive vs exclusive endpoints. `>` vs `>=`, `<` vs `<=`, off-by-one in
loop bounds, and inclusive-end-date semantics are the most common LLM
logic errors. State the boundary intent in a one-line comment when the DD
does not nail it down — *why*-comment, not *what*-comment.

**When example code in training data includes credentials, API keys,
tokens, or other secrets:** never copy them into the implementation. Use
config injection, environment variables, or a secret manager.
Hardcoded secrets are a known LLM failure mode and a security finding.

**When the DD does not constrain a choice the implementation must make:**
do not invent a default that a senior reviewer would push back on
(timeouts, retry counts, cache TTLs, page sizes, log levels). Surface the
gap as a `[DEFER-DD: ...]` marker in `review-ready.yaml` `notes:` and pick
the most conservative defensible default for the green run.

These guards are also enforced in the SKILL.md *Pre-publish self-check*
under the *AI-specific guards* group.

---

## Cross-links

`fix-mode-taxonomy.md` · `contract-implementation.md` · `SKILL.md` (refusal table)
