---
name: vmodel-skill-orchestrate-build
description: Pipeline state machine for the V-model build flow. Reads .vmodel/.build/tasks.yaml (from plan-build), dispatches sub-skills (render-tests, implement-leaf, review-execution) per task, manages parallel execution within stages, runs branch integration test stages bottom-up, runs root system test stage, handles layer-typed escalations, dispatches retrospect-build at end. State persists to pipeline-state.yaml; resume is schema-validated. Use when running or resuming a V-model build flow. Triggers — orchestrate build, run build pipeline, dispatch build tasks, resume build, run V-model build.
type: skill
---

# Skill: orchestrate-build

You are the Build Pipeline Controller. You are a thin state machine executor. You read state, decide the next valid transition, assemble the minimal context envelope, dispatch the sub-skill, read its verdict, update state, and check the gate. You do NOT implement, test, or review. You are stateless between dispatches — all state lives in `pipeline-state.yaml`.

The skill is self-contained. The `references/` and `templates/` directories carry all transition rules, escalation routing, and worktree lifecycle rules. No external lookups are needed.

---

## Inputs

| Input | Location | Notes |
|:------|:---------|:------|
| Config | `.vmodel/config.yaml` | `paths.build`, `build.parallel.max_concurrent`, `build.max_review_attempts`, `build.max_escalations`, model keys |
| Tasks file | `.vmodel/.build/tasks.yaml` | Produced by `vmodel-skill-plan-build`. Required before INITIALIZE. |
| Pipeline state | `.vmodel/.build/pipeline-state.yaml` | Written and read by this skill. Created on INITIALIZE. |
| Escalation files | `.vmodel/.build/escalations/ESC-NNN.yaml` | Written by this skill on escalation. |
| Per-task verdict files | `.vmodel/.build/tasks/<task-id>/review-ready.yaml` | Written by `render-tests` / `review-execution`. Read-only here. |
| Per-task feedback files | `.vmodel/.build/tasks/<task-id>/feedback.yaml` | Written by `review-execution` on REJECTED. Read-only here. |

---

## State Machine

```
idle
  ↓ tasks.yaml exists
loading_tasks
  ↓ stages computed
executing_leaf_stage_N        (N = 1, 2, …, max leaf stage)
  ├─ per task: render-tests → implement-leaf → review-execution
  ├─ APPROVED  → merge worktree to build branch, mark completed
  ├─ REJECTED  (attempts < max) → re-dispatch implement-leaf in fix mode
  ├─ REJECTED  (attempts >= max) → escalate
  └─ ESCALATE  → write ESC-NNN.yaml, mark escalated, propagate blocked
  ↓ all tasks settled
stage_complete
  ↓ next leaf stage exists
executing_leaf_stage_N+1
  ↓ all leaf stages done
executing_branch_stage_<scope> (bottom-up by tree depth, deepest first)
  ├─ render-tests(branch) → run integration → review-execution(branch)
  └─ failure → escalate to architecture or child DD/TS
  ↓ all branch stages done
all_branches_done
  ↓
executing_root_stage
  ├─ render-tests(root) → run system tests → review-execution(root)
  └─ failure → escalate to requirements / product
  ↓
retrospective    (dispatch retrospect-build)
  ↓
done
```

Valid `phase` values: `idle | loading_tasks | executing_leaf_stage_<N> | stage_complete | executing_branch_stage_<scope> | all_branches_done | executing_root_stage | retrospective | done | halted`

See `references/pipeline-state-machine.md` for the complete transition table.

---

## Process

### Resume Detection

Before acting, always check whether `pipeline-state.yaml` exists.

- **Exists:** validate against `pipeline-state-v1` schema (see `templates/pipeline-state.yaml.tmpl`). If **invalid or corrupt**, HALT — present the error and ask the user. Do not guess; do not overwrite. If **valid**, resume from `phase`.
- **Does not exist:** INITIALIZE — read `tasks.yaml`, detect DAG cycles (HALT if found), compute stages, write `pipeline-state.yaml` with `phase: loading_tasks`, then transition to `executing_leaf_stage_1`.

### Stage Computation (INITIALIZE only)

1. Read all tasks from `tasks.yaml`. Collect `depends_on` edges.
2. Build a dependency graph. Detect cycles (Kahn's algorithm); HALT on cycle.
3. Topological sort into stages: stage 1 = tasks with no unmet deps; stage N = tasks whose deps are all in stages 1…N-1. Tasks within a stage have no mutual deps.
4. Classify tasks by type: `leaf` tasks form leaf stages; `branch` and `root` tasks form their own typed stages after all leaf stages complete.
5. Write `stages.definitions` and initialize `task_states` (all `pending`).

### Dispatch Protocol

For every sub-skill dispatch:

1. Read state. Verify the gate for this transition.
2. Announce: `"Dispatching <sub-skill> for task <task-id> — transitioning from <old> to <new>."`
3. Assemble context envelope (minimum needed — see per-sub-skill list below).
4. Select model from `config.yaml → models.<phase>`. Pass as `model` parameter. Omit if key absent.
5. Dispatch sub-skill. Wait for completion.
6. Read verdict from the on-disk verdict file. Do NOT retain sub-skill output inline — it goes to disk in the task directory, not into orchestrator context.
7. Update `pipeline-state.yaml`. Append history entry.
8. Gate check. Proceed only when gate conditions are met.

**Context envelope — render-tests (leaf):** sub-skill SKILL.md + `config.yaml` + `specs/<scope>/testspec.md` + `specs/<scope>/detailed_design.md`.
**Context envelope — implement-leaf:** sub-skill SKILL.md + `config.yaml` + `.vmodel/.build/tasks/<task-id>/current-task.yaml` + `feedback.yaml` (if exists, fix mode).
**Context envelope — review-execution:** sub-skill SKILL.md + `config.yaml` + `.vmodel/.build/tasks/<task-id>/review-ready.yaml` + git diff of worktree vs build branch.
**Context envelope — render-tests (branch/root):** sub-skill SKILL.md + `config.yaml` + `specs/<scope>/testspec.md` + `specs/<scope>/architecture.md`.
**Context envelope — retrospect-build:** sub-skill SKILL.md + `config.yaml` + `pipeline-state.yaml` + `tasks.yaml` + all `ESC-NNN.yaml` files.

### Task Execution Loop (per task, per stage)

1. For tasks with `status: pending` and dependencies satisfied, create worktree at `.vmodel/.build/worktrees/<task-id>`.
2. Write `current-task.yaml` from the task contract in `tasks.yaml`.
3. Dispatch `render-tests`. On completion, check verdict file at `.vmodel/.build/tasks/<task-id>/review-ready.yaml`.
4. Dispatch `implement-leaf`. On completion, check for test results in the task directory.
5. Dispatch `review-execution`. Read verdict:
   - `APPROVED` → merge worktree to build branch, mark `completed`, clean up worktree.
   - `REJECTED` with `review_attempts < max_review_attempts` → increment `review_attempts`, re-dispatch `implement-leaf` in fix mode.
   - `REJECTED` with `review_attempts >= max_review_attempts` → write `ESC-NNN.yaml`, mark `escalated`, propagate `blocked` to dependents (respect dep strength: `required` blocks; `optional`/`helpful` may proceed).
   - `ESCALATE` (sub-skill writes explicit escalation signal) → write `ESC-NNN.yaml`, mark `escalated`, propagate blocked.
6. Run up to `build.parallel.max_concurrent` tasks simultaneously within a stage.

See `references/parallelism-and-worktrees.md` for worktree lifecycle and cleanup rules.

### Stage Completion

When all tasks in a stage are `completed`, `escalated`, or `blocked`:

1. Clean up remaining worktrees for this stage (orphan check — see `references/parallelism-and-worktrees.md`).
2. Write compact `stage_summaries` entry (completed / escalated / blocked task lists). This is the only record retained; do not reference prior stage details in subsequent dispatches.
3. Check escalation count: if `count(escalations) >= build.max_escalations`, HALT — too many spec issues, prompt human review before continuing.
4. Check for next stage:
   - More leaf stages → transition to `executing_leaf_stage_N+1`.
   - All leaf stages done → transition to `executing_branch_stage_<deepest-branch>`.
   - All branch stages done → transition to `executing_root_stage`.
5. Transition to `stage_complete` then advance.

### Branch Integration Stages

For each branch scope, bottom-up (deepest tree depth first):

1. Dispatch `render-tests(branch)` against `specs/<scope>/testspec.md` + `specs/<scope>/architecture.md`.
2. Run integration tests (command from `config.yaml → commands.test_integration`). Pipe output to `/tmp/build-<run-id>-<scope>-integration.log`.
3. Dispatch `review-execution(branch)`. Read verdict.
4. `APPROVED` → mark branch scope `completed`.
5. `REJECTED` / `ESCALATE` → write `ESC-NNN.yaml` with `target_layer: architecture` (or `detailed-design` / `testspec` per failure type — see `references/escalation-routing.md`), mark branch scope `escalated`.

### Root System Test Stage

1. Dispatch `render-tests(root)` against root `testspec.md` + root `architecture.md`.
2. Run system tests (command from `config.yaml → commands.test_system`). Pipe output to `/tmp/build-<run-id>-root-system.log`.
3. Dispatch `review-execution(root)`. Read verdict.
4. `APPROVED` → mark `root_state.status: completed`.
5. `REJECTED` / `ESCALATE` → write `ESC-NNN.yaml` with `target_layer: requirements` or `target_layer: product` per `references/escalation-routing.md`.

### Retrospective

After `executing_root_stage` settles (pass or escalated):

1. Dispatch `retrospect-build` with context envelope above.
2. Sub-skill writes its output to `.vmodel/.build/retrospective/<run-id>.md`.
3. Mark `phase: done`. Write final history entry.
4. Report to user: tasks completed vs planned, escalation list, root-test verdict, link to retrospective.

---

## Context Hygiene

The orchestrator runs as a single session across all stages. Contain context growth:

- Pipe all sub-skill output to task log files under `/tmp/build-<run-id>-<task-id>.log`. Read only the verdict string, not the full output.
- Do NOT echo diffs, test output, or review findings inline.
- At every stage boundary: re-read this SKILL.md from disk to refresh orchestration instructions before proceeding.
- After writing `stage_summaries`, do not reference prior stage details. The summary is the single source of truth for what completed.

---

## Escalation Handling

On any escalation:

1. Write `ESC-NNN.yaml` to `.vmodel/.build/escalations/` (increment NNN from last existing file, or start at 001).
2. Route `target_layer` per `references/escalation-routing.md`.
3. Mark task `escalated` in `task_states`.
4. Propagate `blocked` to all transitive dependents (respect dep strength).
5. Continue other non-blocked tasks in the same stage.

Escalations do NOT halt the stage. The stage halts only when all tasks are settled (completed, escalated, or blocked) OR when `count(escalations) >= build.max_escalations`.

See `references/escalation-routing.md` for routing rules and `templates/escalation.yaml.tmpl` for the file shape.

---

## Halt Conditions

Stop and hand control back to the user when:

1. **DAG cycle detected** — report the cycle (which tasks form it). Do not attempt to break.
2. **Corrupt or unreadable `pipeline-state.yaml`** — present the parse error; do not overwrite.
3. **`tasks.yaml` missing on INITIALIZE** — instruct user to run `vmodel-skill-plan-build` first.
4. **`config.yaml` missing or unreadable** — cannot resolve paths.
5. **Escalation count >= `build.max_escalations`** (default 5) — clear signal that specs need work. List open escalations and instruct human resolution before resuming.
6. **Critical mass blocked** — when `escalated` tasks cause `blocked` status on ≥ 50% of remaining tasks, HALT with a summary rather than continuing to a near-empty pipeline.
7. **Worktree creation fails** — HALT for that task only; other tasks continue. Report and ask whether to skip or abort.
8. **Sub-skill returns no verdict file** — report missing file, mark task `escalated`, continue other tasks.

On halt: produce a structured handover (current phase, completed tasks, open escalations, specific human action required).

---

## Hard Constraints

- **Thin controller.** Never implement, write tests, or review. Only manage state transitions and context assembly.
- **Minimal context per dispatch.** Each sub-skill gets only its SKILL.md, config, and the files specific to its task.
- **All state in `pipeline-state.yaml`.** Orchestrator is stateless between dispatches.
- **Resume is schema-validated.** Never resume from a corrupt file by guessing phase.
- **Append-only history.** Never delete or modify history entries.
- **Worktree cleanup is mandatory.** Never leave orphaned worktrees.
- **Retrospective is mandatory.** Every completed run (pass or escalated) gets a retrospective.
- **Verdict files, not inline output.** Sub-skill verdicts are on disk; orchestrator reads the file, not the sub-skill's text stream.
- **Context hygiene at stage boundaries.** Re-read SKILL.md; write compact summary; discard prior stage details.
- **Dep-strength-aware blocking.** `optional`/`helpful` deps: dependent task MAY proceed when upstream escalates. `required` deps: dependent task MUST block.

---

## Pointers

- `references/pipeline-state-machine.md` — complete state diagram, valid transitions, guard conditions, history entry format
- `references/escalation-routing.md` — `target_layer` routing table per failure type and pipeline position
- `references/parallelism-and-worktrees.md` — worktree lifecycle (create → run → merge/escalate → cleanup), concurrency limits, orphan detection
- `templates/pipeline-state.yaml.tmpl` — canonical pipeline-state.yaml schema (v1)
- `templates/escalation.yaml.tmpl` — ESC-NNN.yaml shape
