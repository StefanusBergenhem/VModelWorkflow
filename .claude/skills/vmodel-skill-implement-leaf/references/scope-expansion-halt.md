---
purpose: Detection points and emit procedure for build-blocked.yaml when implement-leaf hits a contract boundary it cannot cross.
audience: vmodel-skill-implement-leaf
status: active
---

# Scope-expansion HALT

**Contents.** When to halt · Detection points · Emit procedure ·
suggested_resolution selection · What NOT to do · Cross-links.

---

## 1. When to halt

Halt and emit `build-blocked.yaml` whenever the natural implementation requires
crossing one of the contract boundaries supplied by the orchestrator in
`current-task.yaml`:

- Reading a file outside `context_to_load` (and not a project source file or
  rendered test file).
- Writing a file outside `files_to_touch` (and not within the leaf's own
  source directory by project convention).
- Performing an action explicitly forbidden by an `out_of_scope` entry.

Hitting such a boundary is the explicit signal: the implementer cannot decide
to expand scope. Only the orchestrator can amend the contract, and only the
human can revise the spec.

---

## 2. Detection points

Three places where a boundary may surface mid-attempt:

1. **On first scan of the DD.** If the DD plainly requires touching files
   clearly outside the scope's source directory (per project conventions),
   emit `build-blocked.yaml` before writing any code. Do not start work
   speculatively.

2. **During the green/refactor loop.** If a needed change crosses a boundary
   (for example, a refactor to extract a shared utility into a sibling leaf's
   directory), halt immediately. Do not silently expand. The TDD loop is not
   a license to grow the scope.

3. **On reading.** If a piece of context — a sibling's interface, a config
   schema, a library version document — is required and not in
   `context_to_load`, halt before opening the file.

---

## 3. Emit procedure

1. Stop work. Do not continue speculatively.
2. Fill `templates/build-blocked.yaml.tmpl` with the specific blocker:
   - `blocker_type` — one of: `scope-expansion`, `missing-context`,
     `contradiction`, `test-defect`, `external-dep`.
   - `blocker_description` — one sentence.
   - `needed_writes[]` — required when `blocker_type: scope-expansion`. Path
     plus reason for each file.
   - `needed_reads[]` — required when `blocker_type: missing-context`. Path
     plus reason.
   - `evidence[]` — at least one entry: file, line, verbatim quote.
3. Choose `suggested_resolution` honestly (see §4).
4. Write to `.vmodel/.build/tasks/<task-id>/build-blocked.yaml`.
5. Do NOT write `review-ready.yaml`. Do NOT commit partial code.
6. Update `build-progress.yaml` with the current `last_step` (whichever gate
   was active when the halt fired) and `note: "halted — see build-blocked.yaml"`.

The orchestrator decides what happens next: auto-amend the contract (if
allowed and within the leaf's scope directory) or escalate to the responsible
spec layer.

---

## 4. Choosing `suggested_resolution`

Pick the value that matches what would actually unblock the work — do not
optimise for "fastest path" or "least disruption":

| Value | Use when |
|---|---|
| `amend-contract` | The expansion is small (1–2 files) and clearly within the spirit of the DD. The orchestrator may auto-add the paths to `context_to_load` / `files_to_touch` if they fall within the leaf's source directory. |
| `escalate-to-dd` | The DD genuinely does not say what to do for the case the implementation hit. The right fix is a DD revision. |
| `escalate-to-architecture` | Interface contracts between leaves are unclear or contradictory at the architecture level. |
| `escalate-to-testspec` | A rendered test contradicts the DD (the test is wrong). Pair with `blocker_type: test-defect`. |
| `escalate-to-adr` | The work surfaces a cross-cutting decision not captured by any existing ADR. |

Be honest. Suggesting `amend-contract` for what is really a DD gap will
result in the orchestrator escalating anyway when the auto-amend heuristic
fails (paths outside the leaf's source directory) — and you have wasted a
round trip.

---

## 5. What NOT to do

- Do NOT modify your own `current-task.yaml`. The contract is read-only to
  this skill. Even when you suggest `amend-contract`, the orchestrator owns
  the amendment.
- Do NOT continue implementing past the boundary "just to see if tests
  pass". A passing build that violated the contract is not approved work —
  review-execution will reject it as `scope-violation`.
- Do NOT delete the failing test or weaken the assertion to remove the
  pressure. That is refusal G + `out_of_scope` rule 2.
- Do NOT write a partial `review-ready.yaml` with notes of what was missed.
  The handoff contract is binary: a leaf is either review-ready or blocked.

---

## Cross-links

`SKILL.md §Scope-expansion HALT` ·
`SKILL.md §Refusals (Refusal H)` ·
`templates/build-blocked.yaml.tmpl` ·
`vmodel-skill-orchestrate-build/SKILL.md §Task Execution Loop step 4a` ·
`vmodel-skill-orchestrate-build/references/escalation-routing.md §Scope-expansion routing`
