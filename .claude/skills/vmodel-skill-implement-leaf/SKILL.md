---
name: vmodel-skill-implement-leaf
description: Implement code for one leaf scope using TDD green phase plus refactor. Inputs are a leaf's Detailed Design (DbC contracts, data invariants, algorithms, state, error matrix), TestSpec, already-rendered failing tests, and governing ADRs; output is code that makes the tests pass, satisfies the DD's contracts, and respects ADR constraints. Operates in greenfield (new code) or fix mode (re-implement after a review-execution rejection — taxonomy-driven, max retry from config). Refuses to implement features not in the DD, contradict ADRs, weaken tests, or skip refactor. Triggers — implement leaf, write code from DD, TDD green phase, fix implementation rejection, V-model leaf implementation.
type: skill
---

# vmodel-skill-implement-leaf

Implement production code for one leaf scope. The DD is the spec; tests are the
verification. The skill runs the TDD green phase plus refactor loop, strictly
bounded by the DD's contracts and the governing ADRs.

All procedure, taxonomy, and contract-translation rules live in the
`references/` directory. This file describes when to use the skill, what it
needs, what it produces, and when to refuse or halt.

## When to use

Activate this skill when:

- A leaf scope has an approved DD, an approved TestSpec, and rendered (failing)
  tests ready
- The user asks to implement, write code, or run the TDD green phase for a leaf
  scope
- A prior review-execution returned a rejection and the user asks to fix the
  implementation

Do **not** activate this skill for:

- Authoring or revising spec artifacts — use the appropriate author skills
- Rendering test files from TestSpec cases — use `vmodel-skill-render-tests`
- Reviewing the resulting code — use `vmodel-skill-review-code`
- Non-leaf scopes — implementation at non-leaf scope is architecture-level wiring
  (out of scope here)

## Inputs

Ask for anything missing. HALT (refusal A) if DD or rendered tests are absent.

| Input | Location | Required |
|---|---|---|
| Detailed Design | `<leaf-scope>/detailed_design.md` | Yes — refusal A if absent |
| TestSpec | `<leaf-scope>/testspec.md` | Yes — refusal A if absent |
| Rendered (failing) tests | project test source tree | Yes — refusal A if absent |
| Governing ADRs | paths in DD front-matter `governing_adrs` | Yes — refusal B if referenced but unreadable |
| `.vmodel/config.yaml` | project root | Yes — for `commands.test`, `commands.lint`, `build.retry.max_review_attempts` |
| Project conventions | `.vmodel/references/` + project-side `conventions.md` | Optional; match existing patterns when present |
| `feedback.yaml` (fix mode) | `.vmodel/.build/<task-id>/feedback.yaml` | Fix mode only — refusal C if missing in fix mode |

## Output

Source code file(s) implementing the leaf scope, plus one YAML status file.

**`review-ready.yaml`** written to `.vmodel/.build/<task-id>/review-ready.yaml`.
Template: `templates/review-ready.yaml.tmpl`.

## Procedure

Mode is **greenfield** (default) or **fix** (when `feedback.yaml` is present).

### Greenfield

Full procedure: `references/tdd-green-and-refactor.md`.

Summary:

1. Read DD completely: every Public Interface entry, every Data Structure, every
   Algorithm, state machine, error matrix. Parse the full contract set before
   writing one line.
2. Read TestSpec cases for orientation. Do NOT implement to the tests; implement
   to the DD. Tests are verification, not the spec.
3. Read governing ADRs. Extract constraints (technology choices, forbidden
   patterns, required patterns). Any constraint that blocks implementation is a
   HALT (refusal D).
4. Read `.vmodel/config.yaml` and project conventions. Match file layout and
   naming to existing patterns.
5. Write minimum code to satisfy the DD's contracts. Do not add features the DD
   does not specify.
6. Run tests (`commands.test`). Iterate until all pass.
7. Refactor: apply DD's data-structure invariants, thread-safety category, error
   matrix, and complexity limits. Tests passing on first attempt is not a reason
   to skip refactor — the DD's structural properties are always enforced.
8. Run lint (`commands.lint`) and coverage if configured.
9. Run the pre-publish self-check (see Pre-publish self-check below).
10. Write `review-ready.yaml`.

### Fix mode

Full procedure: `references/fix-mode-taxonomy.md`.

Summary:

1. Read `feedback.yaml`. It contains typed rejection entries.
2. For each entry, apply the per-type response (taxonomy in `fix-mode-taxonomy.md`).
3. Re-run tests and lint.
4. Run pre-publish self-check.
5. Re-emit `review-ready.yaml` with `notes:` referencing addressed feedback entries.
6. If attempt count reaches `build.retry.max_review_attempts` and rejections remain
   unresolvable at this layer, HALT and surface escalation (refusal E).

## Pre-publish self-check

Before writing `review-ready.yaml`, verify each item. Fail = do not emit, fix
first.

```
[ ] Every Public Interface entry has a corresponding implementation
[ ] No implementation feature absent from the DD
[ ] Each ADR constraint is honoured
[ ] Complexity limits met (function ≤50 lines, cyclomatic ≤10, nesting ≤3)
[ ] Error handling follows DD's error matrix (no null returns, no empty catches)
[ ] Thread-safety per DD's spec (Goetz category honoured)
[ ] Data structure invariants enforced in constructors / factory methods
[ ] No test weakened or deleted to achieve green
[ ] Lint: clean
[ ] Coverage thresholds met (if configured)
```

## Refusals

| ID | Condition | Action |
|---|---|---|
| A | DD or rendered tests absent | HALT. State what is missing; do not proceed. |
| B | Governing ADR referenced in DD but unreadable | HALT. List missing ADRs; request paths. |
| C | Fix mode invoked but `feedback.yaml` absent | HALT. Request path to `feedback.yaml`. |
| D | ADR constraint makes correct implementation impossible | HALT. Describe the contradiction; request ADR revision. |
| E | `max_review_attempts` exhausted, rejections remain | HALT. Surface unresolvable entries; escalate to architecture review or spec revision. |
| F | User requests a feature not in the DD | HALT. "Not in DD. Add to DD first, then re-invoke." |
| G | Test is wrong — fixing it would make tests pass but violate DD | HALT. Escalate to `vmodel-skill-author-testspec` / `vmodel-skill-render-tests`; do not weaken or delete. |
| H | Integration failure surfaces (unit-level tests pass, composition fails) | HALT. Escalate to architecture review; this layer cannot resolve integration concerns. |
