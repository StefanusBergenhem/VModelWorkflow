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
- Reviewing the resulting code or build output — use `vmodel-skill-review-execution`
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
| `feedback.yaml` (fix mode) | `.vmodel/.build/tasks/<task-id>/feedback.yaml` | Fix mode only — refusal C if missing in fix mode |

## Output

Source code file(s) implementing the leaf scope, plus one YAML status file.

**`review-ready.yaml`** written to `.vmodel/.build/tasks/<task-id>/review-ready.yaml`.
Template: `templates/review-ready.yaml.tmpl`. This is the implementation handoff;
`vmodel-skill-review-execution` reads it (alongside the git diff and test
results) to produce the verdict.

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

**Contract & DD compliance**
```
[ ] Every Public Interface entry has a corresponding implementation
[ ] No implementation feature absent from the DD (no gold plating)
[ ] Each ADR constraint is honoured
[ ] Error handling follows DD's error matrix (no null returns where forbidden,
    no empty catches, typed errors only)
[ ] Thread-safety per DD's spec (Goetz category honoured)
[ ] Data structure invariants enforced in constructors / factory methods
```

**Code quality (from craft guide)**
```
[ ] Complexity: function length ≤50 lines (target 5–15), cyclomatic ≤10,
    nesting ≤3, parameters ≤5 (target 0–3; parameter object above 5),
    file ≤500 lines
[ ] No magic numbers — numeric/string literals carrying domain meaning are
    named constants
[ ] Comments explain *why*, not *what* — no comments restating the code
[ ] Resources cleaned up (try-with-resources / defer / RAII as language allows)
[ ] No dead code, no commented-out code, no TODO stubs for unspecified features
```

**AI-specific guards (LLM failure modes from craft guide §3.4)**
```
[ ] Every external API call (method, signature, return type) verified against
    the actual library version in use — no plausible-but-fictional methods
[ ] Every configuration property name verified against its framework's actual
    schema — no hallucinated keys
[ ] Boundary conditions inspected for off-by-one (inclusive vs exclusive,
    `>` vs `>=`, range endpoints)
[ ] No hardcoded credentials, API keys, tokens, or other secrets — use config
    injection / environment variables / secret managers
```

**Test & build hygiene**
```
[ ] No test weakened, disabled, or deleted to achieve green
[ ] Lint: clean (no suppressions added without DD-cited justification)
[ ] Coverage thresholds met (if configured)
```

## Refusals

Each row below is a HALT condition. When the condition fires, the skill stops,
emits the structured handover, and does not write `review-ready.yaml`.

| ID | Condition | Action |
|---|---|---|
| A | DD or rendered tests absent | HALT. State what is missing; do not proceed. |
| B | Governing ADR referenced in DD but unreadable | HALT. List missing ADRs; request paths. |
| C | Fix mode invoked but `feedback.yaml` absent | HALT. Request path to `feedback.yaml`. |
| D | ADR constraint makes correct implementation impossible | HALT. Describe the contradiction; request ADR revision. |
| E | `max_review_attempts` exhausted, rejections remain | HALT. Surface unresolvable entries; escalate to architecture review or spec revision. |
| F | User requests a feature not in the DD | HALT. "Not in DD. Add to DD first, then re-invoke." |
| G | Test is wrong — fixing it would make tests pass but violate DD | HALT. Escalate to `vmodel-skill-author-testspec` / `vmodel-skill-render-tests`; do not weaken or delete. |
