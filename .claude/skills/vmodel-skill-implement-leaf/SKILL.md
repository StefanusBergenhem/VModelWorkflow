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
| `current-task.yaml` | `.vmodel/.build/tasks/<task-id>/current-task.yaml` | Yes — carries the contract (`acceptance_criteria`, `context_to_load`, `out_of_scope`) plus `mode` / `attempt` / optional resume hint |
| Resume hint | `current-task.yaml` `mode: resume` + `resume_from_step` field | Set by orchestrator on detecting a mid-attempt crash — triggers Resume mode |

## Output

Source code file(s) implementing the leaf scope, plus one YAML status file.

**`review-ready.yaml`** written to `.vmodel/.build/tasks/<task-id>/review-ready.yaml`.
Template: `templates/review-ready.yaml.tmpl`. This is the implementation handoff;
`vmodel-skill-review-execution` reads it (alongside the git diff and test
results) to produce the verdict.

**`build-progress.yaml`** written to `.vmodel/.build/tasks/<task-id>/build-progress.yaml`.
Template: `templates/build-progress.yaml.tmpl`. Overwrite-on-update at every gate
boundary; the orchestrator reads this on resume to decide recovery path.

**`build-blocked.yaml`** written to `.vmodel/.build/tasks/<task-id>/build-blocked.yaml`
ONLY when the implementation hits a contract boundary it cannot cross
(scope-expansion, missing-context, contradiction, test-defect, external-dep).
Template: `templates/build-blocked.yaml.tmpl`. When this file is emitted, do NOT
emit `review-ready.yaml`. The orchestrator decides auto-amend vs escalate.

## Contract enforcement

The orchestrator-supplied `current-task.yaml` carries three contract fields that
constrain this skill's behaviour. Enforcement is mandatory:

- **`acceptance_criteria`** — informational list of TestSpec case references the
  implementation must satisfy. Use to verify coverage before emitting
  `review-ready.yaml`. Do not cite as design source — the DD is the spec.

- **`context_to_load`** — read-only allowlist of spec / reference files. Refuse
  to Read any file outside this list except:
    (a) source code files in the project (the implementation surface)
    (b) the rendered test files in the worktree
  Reading anything else (other leaves' source, unrelated specs, third-party
  config) is a scope violation — emit `build-blocked.yaml` (see Refusal H and
  the *Scope-expansion HALT* section).

- **`out_of_scope`** — declarative do-not list. Treat each entry as a HALT
  trigger if the natural implementation would require crossing the boundary.
  Emit `build-blocked.yaml` with the matching `blocker_type`.

→ Full procedure for emitting `build-blocked.yaml` and choosing
`suggested_resolution`: `references/scope-expansion-halt.md`.

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

At every gate boundary, overwrite `build-progress.yaml` with the new
`last_step` value (see *Progress checkpointing* below). At any point during
steps 1–10 a contract boundary may surface — see *Scope-expansion HALT*.

### Resume mode

Triggered when `current-task.yaml` has `mode: resume` and `resume_from_step` is
set (orchestrator sets these on detecting a mid-attempt crash with all gates
green but no `review-ready.yaml`).

Procedure:

1. Read `build-progress.yaml`; verify `last_step` matches `resume_from_step`.
2. Re-run all gates from `resume_from_step` forward. Do not redo earlier work.
3. Specifically: do not re-run TDD red; do not re-implement; just re-validate
   gates (lint, coverage, self-check) and write `review-ready.yaml`.
4. Update `build-progress.yaml` at each gate as in greenfield mode.
5. If a gate fails on resume (e.g., lint passes initially but the resumed
   environment fails), drop to a fresh attempt: emit ESC if no progress.

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

## Scope-expansion HALT

When the implementation hits a contract boundary it cannot cross — needing to
read a file outside `context_to_load`, write a file outside `files_to_touch`,
or violate an `out_of_scope` rule — emit `build-blocked.yaml` and halt.

Detection points:

1. On first scan of the DD: if the DD requires touching files clearly outside
   the scope's source directory (per project conventions), emit before writing
   any code.
2. During the green/refactor loop: if a needed change crosses a boundary, halt
   immediately. Do not silently expand.
3. On reading: if a piece of context (a sibling's interface, a config schema,
   a library version document) is required and not in `context_to_load`, halt.

Procedure:

1. Stop work. Do not continue speculatively.
2. Fill `templates/build-blocked.yaml.tmpl` with the specific blocker.
3. Choose `suggested_resolution` honestly:
   - `amend-contract` only when the expansion is small (1–2 files) and clearly
     within the spirit of the DD.
   - `escalate-to-dd` when the DD genuinely does not say what to do.
   - `escalate-to-architecture` when interface contracts between leaves are
     unclear or contradictory.
   - `escalate-to-testspec` when a rendered test contradicts the DD.
4. Write to `.vmodel/.build/tasks/<task-id>/build-blocked.yaml`.
5. Do NOT write `review-ready.yaml`. Do NOT commit partial code.

Auto-amendment is the orchestrator's call, not yours. Even if you suggest
`amend-contract`, do not modify your own `context_to_load` or `files_to_touch`.

→ Full reference: `references/scope-expansion-halt.md`.

## Progress checkpointing

After every gate boundary, overwrite `build-progress.yaml` in the task dir
with the new `last_step`, `last_step_at` (current UTC ISO 8601), and updated
`gates` block. This is mandatory — the orchestrator uses it to decide how to
resume after an interrupted attempt.

Gate boundaries that update `last_step`:

- `started`               → after first read of `current-task.yaml`
- `dd-parsed`             → after DD parsing complete
- `contract-checked`      → after enforcing `context_to_load` / `out_of_scope`
- `files-planned`         → after populating `files_to_touch`
- `red-confirmed`         → after running tests and verifying expected failures
- `green-passing`         → after tests pass for the first time
- `refactored`            → after refactor pass; tests still green
- `lint-clean`            → after lint passes
- `coverage-met`          → after coverage threshold met (or skipped)
- `self-check-passed`     → after pre-publish self-check passes
- `review-ready-written`  → after writing `review-ready.yaml`

Overwrite-on-update — not append. Latest state is authoritative.

Template: `templates/build-progress.yaml.tmpl`.

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
| H | Scope expansion required — implementation needs to read or write a file outside the contract's allowlist (`context_to_load` / `files_to_touch`) or violates an `out_of_scope` rule | HALT. Emit `build-blocked.yaml` per the *Scope-expansion HALT* section. Do not proceed; do not write `review-ready.yaml`. |
