---
name: vmodel-skill-orchestrate-build
description: Pipeline state machine for the V-model build flow. Reads .vmodel/.build/tasks.yaml (from plan-build), dispatches per-task worker agents (render-tests, implement-leaf, review-execution) via the Task tool for isolated parallel execution and the retrospect-build skill at end-of-run, manages parallel execution within stages, runs branch integration test stages bottom-up, runs root system test stage, handles layer-typed escalations. State persists to pipeline-state.yaml; resume is schema-validated. Use when running or resuming a V-model build flow. Triggers — orchestrate build, run build pipeline, dispatch build tasks, resume build, run V-model build.
type: skill
---

# Skill: orchestrate-build

The orchestrator is a thin state machine executor for the build pipeline. It reads pipeline state, decides the next valid transition, assembles the minimal context envelope, dispatches the sub-skill or sub-agent, reads its verdict, updates state, and checks the gate. The orchestrator does not implement, test, or review. It is stateless between dispatches — all state lives in `pipeline-state.yaml`.

The skill is self-contained. The `references/` and `templates/` directories carry all transition rules, escalation routing, and worktree lifecycle rules. No external lookups are needed.

---

## Inputs

| Input | Location | Notes |
|:------|:---------|:------|
| Config | `.vmodel/config.yaml` | `paths.build`, `build.parallel.max_concurrent`, `build.max_review_attempts`, `build.max_escalations`, model keys |
| Tasks file | `.vmodel/.build/tasks.yaml` | Produced by `vmodel-skill-plan-build`. Required before INITIALIZE. |
| Pipeline state | `.vmodel/.build/pipeline-state.yaml` | Written and read by this skill. Created on INITIALIZE. |
| Escalation files | `.vmodel/.build/escalations/ESC-NNN.yaml` | Written by this skill on escalation. |
| Per-task render report | `.vmodel/.build/tasks/<task-id>/render-report.yaml` | Written by `render-tests` (manifest of cases rendered + skipped + compile/red checks). Read-only here. |
| Per-task review-ready file | `.vmodel/.build/tasks/<task-id>/review-ready.yaml` | Written by `implement-leaf` after the green-phase + refactor cycle (the implementation handoff). Read-only here. |
| Per-task feedback files | `.vmodel/.build/tasks/<task-id>/feedback.yaml` | Written by `review-execution` on REJECTED. Read-only here. |
| Per-task current-task | `.vmodel/.build/tasks/<task-id>/current-task.yaml` | Written by this skill at every dispatch (greenfield, fix, resume). Carries the contract (`acceptance_criteria`, `context_to_load`, `out_of_scope`) plus `mode` / `attempt` / optional resume hint. |
| Per-task build-blocked | `.vmodel/.build/tasks/<task-id>/build-blocked.yaml` | Written by `implement-leaf` when it hits a contract boundary it cannot cross. Read by this skill to decide auto-amend vs escalate. |
| Per-task build-progress | `.vmodel/.build/tasks/<task-id>/build-progress.yaml` | Written by `implement-leaf` at every gate boundary. Read by this skill on resume to choose recovery path (silent-recover, resume-at-gate, restart). |

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

For every dispatch (per-task agent via Task tool, or retrospect-build skill via Skill tool):

1. Read state. Verify the gate for this transition.
2. Announce: `"Dispatching <sub-skill> for task <task-id> — transitioning from <old> to <new>."`
3. Assemble context envelope (minimum needed — see per-sub-skill list below).
4. Select model from `config.yaml → models.<phase>`. Pass as `model` parameter. Omit if key absent.
5. Dispatch via Task tool with the corresponding agent type:
   - render-tests dispatches → subagent_type: render-tests
   - implement-leaf dispatches → subagent_type: implement-leaf
   - review-execution dispatches → subagent_type: review-execution
   - retrospect-build still dispatches via Skill tool (single invocation, end of run)

   The Task tool gives each dispatched agent an isolated context window. This
   is what makes within-stage parallelism real (multiple Task calls in one
   message run concurrently).

   For parallel dispatch within a stage: emit multiple Task tool calls in a
   single message (one per task in the slot batch up to build.parallel.max_concurrent).
   Wait for all to settle before reading verdict files.
6. Read verdict from the on-disk verdict file. Do NOT retain sub-skill output inline — it goes to disk in the task directory, not into orchestrator context.
7. Update `pipeline-state.yaml`. Append history entry.
8. Gate check. Proceed only when gate conditions are met.

**Dispatch envelope — render-tests (any layer):**
- worktree_root, task_id, layer (leaf | branch | root)
- testspec_path (absolute), parent_spec_path (DD for leaf, ARCH for branch/root)
- config_path (.vmodel/config.yaml absolute)

**Dispatch envelope — implement-leaf:**
- worktree_root, task_id, current_task_path (absolute)
- mode (greenfield | fix | resume), attempt
- feedback_path (when mode == fix)
- resume_from_step (when mode == resume)
- config_path

**Dispatch envelope — review-execution (leaf):**
- worktree_root, task_id, layer: leaf
- current_task_path, review_ready_path
- spec_paths: detailed_design_path + testspec_path
- git_diff_command (the orchestrator-computed diff command for the worktree)
- test_log_path
- config_path

**Dispatch envelope — review-execution (branch):**
- worktree_root, task_id, layer: branch
- current_task_path
- spec_paths: architecture_path + testspec_path
- integration_test_log_path
- git_diff_command
- config_path

**Dispatch envelope — review-execution (root):**
- worktree_root, task_id, layer: root
- current_task_path
- spec_paths: requirements_path + root_product_path + testspec_path + architecture_path
- system_test_log_path
- config_path

**Skill invocation — retrospect-build (single, end of run, NOT via Task tool):**
- Load via Skill tool with: pipeline_state_path, tasks_yaml_path, escalations_dir_path, config_path
- Reason for skill (not agent): runs once at end of run with no parallelism need; orchestrator session is fine.

### Parallel dispatch via Task tool

The orchestrator's true parallelism for a stage comes from emitting multiple
Task tool calls in a single message. Each call dispatches one agent
(implement-leaf / review-execution / render-tests) into an isolated context.

Discipline:
1. Compute the slot batch — the next N pending tasks in the stage where
   N = min(build.parallel.max_concurrent, count(pending tasks)).
2. Emit one Task call per slot in a single tool-use message. Each call:
   - subagent_type: <render-tests | implement-leaf | review-execution>
   - description: "<task-id> <phase>"
   - prompt: the full dispatch envelope (per E.2 above) as a structured prompt
3. Wait for all dispatched agents to return. Read each task's verdict files
   from disk; do NOT inspect agent stdout for state — verdicts are file-based.
4. Update task_states for each settled task; refill slots from the next
   pending tasks until the stage is done.

Sequential fallback (build.parallel.enabled: false): emit one Task call at
a time. Same envelope shape; no batching.

Why agents, not skills, for the per-task workers:
- Isolated context window per task → orchestrator's context budget is not
  consumed by sub-skill output.
- True parallelism within a stage → multiple Task calls in one message run
  concurrently.
- Failure isolation → one agent crash does not affect siblings.

### Task Execution Loop (per task, per stage)

1. For tasks with `status: pending` and dependencies satisfied, create worktree at `.vmodel/.build/worktrees/<task-id>`.
2. Write `current-task.yaml` from the task contract in `tasks.yaml`. Copy verbatim:
   `task_id`, `build_run_id`, `scope`, `task_type`, `detailed_design`, `testspec`, `governing_adrs`, `acceptance_criteria`, `context_to_load`, `out_of_scope`, `depends_on`. Set `mode: greenfield` and `attempt: 1` on first dispatch. On fix-mode re-dispatch (after a REJECTED): set `mode: fix`, increment `attempt`, **append** the fix-mode entry to `out_of_scope`: `"Do not weaken, disable, or delete tests to satisfy feedback — escalate as ESC if the feedback is itself wrong."` (the four planner entries stay; the fifth is appended once). Initialise `files_to_touch: []`, `files_to_touch_max_amendments: <build.auto_amend.max_auto_amendments>`, `amendments_used: 0`. Template: `templates/current-task.yaml.tmpl`.
3. Dispatch the `render-tests` agent (Task tool, subagent_type: render-tests). On completion, check `render-report.yaml` at `.vmodel/.build/tasks/<task-id>/render-report.yaml` — verify `compile_check: passed` and `red_phase_check: all_red`. If render-tests HALTed (e.g., weak oracle), treat as ESCALATE → testspec.
4. Dispatch the `implement-leaf` agent (Task tool, subagent_type: implement-leaf). On completion, verify `review-ready.yaml` exists at `.vmodel/.build/tasks/<task-id>/review-ready.yaml`. Absent file is not necessarily a failure — see step 4a (build-blocked). On resume after a crash, the dispatch envelope may be a resume-mode envelope per `references/pipeline-state-machine.md §Idempotency on Resume`. If neither `review-ready.yaml` nor `build-blocked.yaml` exists and the agent exited normally, mark `escalated` and surface to user.
4a. **Check for `build-blocked.yaml`** in the task dir. If present:
    - Read `suggested_resolution`, `blocker_type`, `needed_writes`, `needed_reads`.
    - If `suggested_resolution == amend-contract` AND `amendments_used < build.auto_amend.max_auto_amendments` AND scope is clearly within the leaf's directory pattern (heuristic: every `needed_writes[].path` is within `<config.paths.src>/<scope>/**`):
      → **Auto-amend.** Append `needed_writes[].path` entries to `current-task.yaml.files_to_touch`; append `needed_reads[].path` entries to `current-task.yaml.context_to_load`; increment `amendments_used`; append a history entry to `pipeline-state.yaml` with `type: contract-amendment` (include the amended paths and the blocker reason). Re-dispatch `implement-leaf` (NOT in fix mode — same `attempt` counter, mode unchanged).
    - Otherwise (suggested_resolution != amend-contract, OR amendments exhausted, OR paths outside the scope's source directory):
      → Treat as ESCALATE. Write `ESC-NNN.yaml` with `target_layer` derived from `suggested_resolution`:
        - `escalate-to-dd` → `detailed-design`
        - `escalate-to-architecture` → `architecture`
        - `escalate-to-testspec` → `testspec`
        - `escalate-to-adr` → `adr`
        - `amend-contract` over budget → `detailed-design` with `routing_note: "auto-amend exhausted (amendments_used=N >= max=M); blocker: <blocker_type>"`.
      → Mark task `escalated`; propagate `blocked` to dependents per dep strength.
5. Dispatch the `review-execution` agent (Task tool, subagent_type: review-execution). Determine verdict by inspecting the task dir AFTER the dispatch returns:
   - **APPROVED** = neither `feedback.yaml` nor a new `ESC-NNN.yaml` was written by review-execution (review-execution emits a single stdout line `APPROVED <task-id>` for the orchestrator log; no verdict file is created). Merge worktree to build branch, mark `completed`, clean up worktree.
   - **REJECTED** = `feedback.yaml` exists. If `review_attempts < max_review_attempts`, increment `review_attempts` and re-dispatch `implement-leaf` in fix mode (per step 2's fix-mode rules). If `review_attempts >= max_review_attempts`, write `ESC-NNN.yaml`, mark `escalated`, propagate `blocked` to dependents (respect dep strength: `required` blocks; `optional`/`helpful` may proceed).
   - **ESCALATE** = a new `ESC-NNN.yaml` is present in the task dir (and copy in `.vmodel/.build/escalations/`). Mark `escalated`, propagate blocked.
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
8. **Sub-skill returns no expected output** — for `render-tests`: missing `render-report.yaml`. For `implement-leaf`: missing `review-ready.yaml`. (For `review-execution`: APPROVED is signalled by the *absence* of a verdict file, so absence is not a failure — only treat as failure if the sub-skill exited with an error or never ran.) Report missing output, mark task `escalated`, continue other tasks.

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
- **Auto-amendment is bounded.** `current-task.yaml.amendments_used <= build.auto_amend.max_auto_amendments` strictly. Escalate beyond that, never silently amend twice.
- **Per-task workers are agents, not skills.** `render-tests`, `implement-leaf`, and `review-execution` are dispatched as agents via the Task tool to give each task an isolated context window. `retrospect-build` is the only sub-step still loaded as a skill (single invocation, end of run).
- **Within-stage parallelism uses concurrent Task calls.** Emit all parallel agent dispatches in a single tool-use message. Do not serialise them.

---

## Pointers

- `references/pipeline-state-machine.md` — complete state diagram, valid transitions, guard conditions, history entry format
- `references/escalation-routing.md` — `target_layer` routing table per failure type and pipeline position
- `references/parallelism-and-worktrees.md` — worktree lifecycle (create → run → merge/escalate → cleanup), concurrency limits, orphan detection
- `templates/pipeline-state.yaml.tmpl` — canonical pipeline-state.yaml schema (v1)
- `templates/escalation.yaml.tmpl` — ESC-NNN.yaml shape
- `templates/current-task.yaml.tmpl` — per-task contract envelope handed to render-tests / implement-leaf / review-execution
- `vmodel-skill-implement-leaf/templates/build-blocked.yaml.tmpl` — handler input for the auto-amend / escalate decision in step 4a
- `vmodel-skill-implement-leaf/templates/build-progress.yaml.tmpl` — per-gate progress checkpoint read on resume
- `.claude/agents/implement-leaf.md` — agent shell that loads `vmodel-skill-implement-leaf`
- `.claude/agents/render-tests.md` — agent shell that loads `vmodel-skill-render-tests`
- `.claude/agents/review-execution.md` — agent shell that loads `vmodel-skill-review-execution`
