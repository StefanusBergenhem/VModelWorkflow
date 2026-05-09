---
purpose: Complete state transition table, guard conditions, history entry format, and stage-boundary rules for the build pipeline state machine.
audience: vmodel-skill-orchestrate-build
status: active
---

# Pipeline State Machine

## State Diagram

```
idle
│  guard: tasks.yaml exists; no pipeline-state.yaml
▼
loading_tasks
│  guard: tasks.yaml readable; DAG has no cycles
▼
executing_leaf_stage_<N>     ←─────────────────────────┐
│  (N = 1 on first entry; increments at stage_complete) │
│  per task loop:                                        │
│    render-tests → implement-leaf → review-execution    │
│    APPROVED   → merge + mark completed                 │
│    REJECTED   (attempts < max) → fix loop              │
│    REJECTED / ESCALATE (attempts >= max) → ESC file   │
│  all tasks settled                                     │
▼                                                        │
stage_complete ──── more leaf stages? ──────────────────┘
│  no more leaf stages
▼
executing_branch_stage_<scope>  (deepest scope first)
│  per scope:
│    render-tests(branch) → integration run → review-execution(branch)
│    APPROVED  → mark branch completed
│    REJECTED/ESCALATE → write ESC, mark branch escalated
│  all branch scopes settled
▼
all_branches_done
▼
executing_root_stage
│  render-tests(root) → system-test run → review-execution(root)
│  APPROVED  → mark root completed
│  REJECTED/ESCALATE → write ESC, mark root escalated
▼
retrospective
│  dispatch retrospect-build
▼
done
```

Special states reachable from any phase:
- `halted` — orchestrator stopped pending human action; written with `halt_reason` in history.

---

## Transition Table

| From | To | Guard / Trigger |
|:-----|:---|:----------------|
| `idle` | `loading_tasks` | `tasks.yaml` present, no `pipeline-state.yaml` |
| `idle` | any phase | `pipeline-state.yaml` valid — resume |
| `loading_tasks` | `executing_leaf_stage_1` | DAG computed, stages written, `task_states` initialized |
| `loading_tasks` | `halted` | Cycle detected or `tasks.yaml` unreadable |
| `executing_leaf_stage_N` | `executing_leaf_stage_N` | Some tasks still `in_progress` |
| `executing_leaf_stage_N` | `stage_complete` | All tasks `completed \| escalated \| blocked` |
| `stage_complete` | `executing_leaf_stage_N+1` | `stages.current < stages.total_leaf` |
| `stage_complete` | `executing_branch_stage_<scope>` | All leaf stages done; branch scopes exist |
| `stage_complete` | `executing_root_stage` | All leaf stages done; no branch scopes |
| `executing_branch_stage_<scope>` | `executing_branch_stage_<next>` | Current branch scope settled; more branch scopes remain (shallower depth) |
| `executing_branch_stage_<scope>` | `all_branches_done` | All branch scopes settled |
| `all_branches_done` | `executing_root_stage` | Automatic |
| `executing_root_stage` | `retrospective` | Root stage settled (pass or escalated) |
| `retrospective` | `done` | `retrospect-build` sub-skill completed |
| any | `halted` | Escalation count >= `build.max_escalations`, or critical-mass blocked, or corrupt state, or cycle |

---

## Guard Conditions Summary

**INITIALIZE guards (before `loading_tasks` → first leaf stage):**
- `tasks.yaml` exists at `paths.build` + `/tasks.yaml`.
- `tasks.yaml` is valid YAML and contains at least one task.
- Dependency graph has no cycles (Kahn's algorithm on `depends_on` fields).
- `config.yaml` is readable.

**RESUME guards (before using existing `pipeline-state.yaml`):**
- `pipeline-state.yaml` parses as valid YAML.
- `version: 1` and `schema: pipeline-state-v1` are present.
- `build_run_id` matches `tasks.yaml → build_run_id` (detect stale state from a different run).
- `phase` value is in the valid-phase enum.

**Stage-advance guards:**
- All tasks in `task_states` for `current_stage` are in a terminal status (`completed | escalated | blocked`).
- Escalation count < `build.max_escalations`.
- `<=` 50% of remaining tasks are in `blocked` status (otherwise critical-mass halt).

**Dispatch guards (per task):**
- Task `status: pending`.
- All `required` dependencies are `completed` (or `optional`/`helpful` deps are anything).
- Worktree path does not already exist (idempotency — on resume, existing worktree means dispatch is in progress; skip re-creation).

---

## History Entry Format

Every state transition appends one entry to `pipeline-state.yaml → history`. Entries are append-only; never deleted.

```yaml
history:
  - phase_from: idle
    phase_to: loading_tasks
    timestamp: "2026-05-09T14:30:00Z"
    reason: "INITIALIZE: tasks.yaml found, no existing state"
  - phase_from: loading_tasks
    phase_to: executing_leaf_stage_1
    timestamp: "2026-05-09T14:30:05Z"
    reason: "4 tasks in 2 stages computed"
  - phase_from: executing_leaf_stage_1
    phase_to: stage_complete
    timestamp: "2026-05-09T14:45:12Z"
    reason: "Stage 1 settled: 2 completed, 0 escalated, 0 blocked"
```

Fields: `phase_from`, `phase_to`, `timestamp` (ISO 8601 UTC), `reason` (one sentence).

For halts, add `halt_reason` (structured object):
```yaml
  - phase_from: executing_leaf_stage_2
    phase_to: halted
    timestamp: "2026-05-09T15:01:00Z"
    reason: "Escalation count reached max_escalations threshold"
    halt_reason:
      type: max_escalations_exceeded
      escalation_count: 5
      open_escalations: [ESC-001, ESC-002, ESC-003, ESC-004, ESC-005]
      required_action: "Resolve open escalations in .vmodel/.build/escalations/, then resume."
```

---

## Stage Boundary Rules

At every `stage_complete` transition, before reading the next stage:

1. **Write compact `stage_summaries` entry.** Format:
   ```yaml
   stage_summaries:
     1:
       completed: [task-id-1, task-id-2]
       escalated: [task-id-3]
       blocked: []
       merged_branches: [build/task-id-1, build/task-id-2]
       settled_at: "2026-05-09T14:45:12Z"
   ```

2. **Clean up worktrees** for all tasks in the settled stage. See `parallelism-and-worktrees.md`.

3. **Re-read this SKILL.md from disk.** Context hygiene — refreshes orchestration instructions in the context window before the next stage begins.

4. **Check escalation count.** If `count(escalations) >= build.max_escalations`, transition to `halted`.

5. **Check critical-mass blocked.** Count remaining `pending` tasks across all unsettled stages. If `blocked_count >= 0.5 * remaining_pending_count`, transition to `halted`.

6. Only after all checks pass: advance to next stage.

---

## Idempotency on Resume

When resuming at `executing_leaf_stage_N`:

- Tasks with `status: completed` → skip (already done).
- Tasks with `status: in_progress` → check whether worktree exists on disk.
  - Worktree exists → the previous dispatch was in progress; re-dispatch from the last-known sub-skill step using the on-disk context files.
  - Worktree does not exist → the state file is ahead of reality (crash before worktree creation); reset to `status: pending` and re-dispatch.
- Tasks with `status: escalated` or `blocked` → skip.
- Tasks with `status: pending` → normal dispatch.

The `review_attempts` counter is authoritative on resume — do not reset it.
