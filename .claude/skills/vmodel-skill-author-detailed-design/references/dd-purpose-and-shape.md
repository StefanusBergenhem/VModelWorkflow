# DD purpose and shape

A DD specifies one leaf scope at the level where code can be implemented and unit tests derived without guessing.

## Position in the scope tree

| Field | What it points to |
|---|---|
| `parent_architecture` | The Architecture artifact whose Decomposition allocates this leaf. **Required** (refusal B). |
| `derived_from` | Upstream artifacts shaping the contract — at least one REQ, optionally sibling DDs / ARCH interfaces / ADRs. **Non-empty**. |
| `governing_adrs` | Cross-cutting decisions inherited or extracted at this leaf. |

Sibling artifact: TestSpec for this leaf. The DD is the source of test derivation.

## Inputs received from parent Architecture

| From parent Architecture | Becomes |
|---|---|
| Decomposition entry's `responsibilities` | DD's Overview content |
| Decomposition entry's interfaces | DD's Public Interface entries |
| Architecture interface invariants | DD invariants (re-stated locally) |
| Parent `governing_adrs` | DD `governing_adrs` (inherited) |
| QA budget allocated to this leaf | DD complexity_notes / performance contracts |

When the parent Architecture is not provided → HALT (refusal B).

## The two rules — both apply simultaneously

| Rule | Statement | Failure → |
|---|---|---|
| **Rule 1** | Do not duplicate what code already shows. | Code paraphrase (refusal C) |
| **Rule 2** | Be specific enough that a junior implements and a tester derives tests. | Spec ambiguity (refusal D) |

Specificity test (all three pass):

1. Two developers reading the DD produce different code (different names, different internal structures).
2. Both implementations pass the same tests.
3. A test engineer writes those tests without ever seeing the code.

Property 3 fails → too vague. Property 1 fails → paraphrasing. Property 2 fails → contract under-specified.

## The success-criteria triple (Spec Ambiguity Test inputs)

| Criterion | Test |
|---|---|
| **Junior-implementable** | A developer unfamiliar with the codebase produces a correct implementation from this DD alone. |
| **Language-portable** | Java / Python / Go implementations from the same DD all satisfy the contract. |
| **Test-derivable** | A test engineer writes the unit-test suite from this DD before code exists. |

Refusal D = all three pass.

## The 7-section shape — every DD

| # | Section | Reference |
|---|---|---|
| 1 | Metadata (front-matter) | `templates/detailed-design.md.tmpl` |
| 2 | Overview | This file |
| 3 | Public Interface | `function-contracts.md` |
| 4 | Data Structures | `data-structures-by-invariant.md` |
| 5 | Algorithms | `algorithms.md` |
| 6 | State | `state-and-concurrency.md` |
| 7 | Error Handling | `error-handling.md` |

When the leaf is stateless → State section is one line: *"Stateless between calls; all state lives in <where>."* Explicit absence is content; missing absence is a defect.

## Overview — what it carries

Two to three paragraphs:

1. What this leaf is and what slice of its parent Architecture it realises.
2. The approach at one level of abstraction above the code (not pseudocode).
3. The leaf's posture relative to siblings (consumer-of-X, producer-of-Y).

Overview carries intent. In retrofit mode, `recovery_status.overview` is narrowed to `verified | unknown` — schema-enforced refusal A. See `retrofit-discipline.md`.

## What does NOT belong in a DD

| Not a … | Why |
|---|---|
| Code paraphrase | Collapses the design box to a point (refusal C). |
| Test substitute | Sibling TestSpec owns tests; DD describes contract the tests verify. |
| Architecture content | Cross-component composition, sibling interfaces — those live at the parent (refusal B). |
| Retrofit invention | Intent / rationale is human-only; mark `unknown` (refusal A). |

## Cross-link

`function-contracts.md` · `data-structures-by-invariant.md` · `algorithms.md` · `state-and-concurrency.md` · `error-handling.md` · `quality-bar-checklist.md` (meta-gate)
