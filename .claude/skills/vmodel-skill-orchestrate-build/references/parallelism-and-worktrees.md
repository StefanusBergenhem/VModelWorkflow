---
purpose: Worktree lifecycle rules, concurrency limits, cleanup protocol, and orphan detection for the build pipeline.
audience: vmodel-skill-orchestrate-build
status: active
---

# Parallelism and Worktrees

## Contents

- [Concurrency model](#concurrency-model)
- [Worktree lifecycle](#worktree-lifecycle)
  - [Create](#create)
  - [Merge (on APPROVED)](#merge-on-approved)
  - [Cleanup](#cleanup)
- [Orphan detection](#orphan-detection)
- [Sub-skill working directory](#sub-skill-working-directory)
- [Sequential fallback](#sequential-fallback)
- [Build branch](#build-branch)

---

## Concurrency model

The orchestrator dispatches multiple tasks simultaneously within a stage, up to `build.parallel.max_concurrent` (read from `config.yaml`; default: 3). Tasks within a stage have no mutual dependencies, making them safe to parallelize.

**Batching.** If a stage has more tasks than `max_concurrent`, process them in batches:
1. Fill a slot batch (size = `max_concurrent`) with the first N pending tasks in the stage.
2. Dispatch all tasks in the batch simultaneously.
3. When any task settles (completed, escalated, or blocked), fill its slot with the next pending task.
4. Continue until all stage tasks are settled.

This is not work-stealing — it is simple slot-filling. No priority ordering within a batch; use task order from `tasks.yaml`.

---

## Worktree lifecycle

Each task gets one git worktree for its full lifecycle (render-tests → implement-leaf → review-execution loop).

### Create

```
Path:  .vmodel/.build/worktrees/<task-id>
Branch: build/<task-id>
Base:   build branch (e.g. build/run-<build-run-id>)
```

Create command pattern (not executed by this skill — described for context envelope to sub-skills that need it):
```
git worktree add <path> -b build/<task-id> <base-branch>
```

After creation, write `current-task.yaml` into the worktree at `.vmodel/.build/worktrees/<task-id>/.vmodel/.build/tasks/<task-id>/current-task.yaml`. This is what sub-skills use to understand their task scope.

**Idempotency on resume.** If the worktree directory already exists when the orchestrator resumes, do not recreate it. The task is `in_progress`; proceed to re-check sub-skill output files.

### Merge (on APPROVED)

1. Merge `build/<task-id>` into the build branch. Fast-forward merge preferred; if not possible, merge commit.
2. If merge conflict arises: HALT for this task (mark `escalated`), escalate to human. Do not auto-resolve.
3. On successful merge: record `merged_branches` entry in the stage summary.

### Cleanup

Clean up the worktree after the task settles (any terminal status: completed, escalated, blocked).

```
git worktree remove --force <path>
git branch -d build/<task-id>   # only if branch already merged; use -D if escalated
```

**Cleanup is mandatory.** Do not skip cleanup because the task was escalated — escalated branches may be revisited by humans but the worktree file system is disposable.

**Cleanup timing.** Clean up immediately after the task settles; do not defer to stage boundary. This prevents accumulating dangling worktrees across a long-running stage.

---

## Orphan detection

An orphaned worktree is a directory under `.vmodel/.build/worktrees/` that exists on disk but has no corresponding `in_progress` or `pending` task in `pipeline-state.yaml → task_states`.

Detect at two moments:
1. **On INITIALIZE** — before starting, scan `.vmodel/.build/worktrees/` for directories. If any exist, it means a previous run left orphans. List them and ask the user whether to clean up (recommended) or abort.
2. **At stage boundaries** — after `stage_complete` cleanup, check that no worktree directories remain for the settled stage. If any do, clean them up and log a warning in the history entry.

Orphan detection is defensive; it must not block the pipeline from resuming.

---

## Sub-skill working directory

Sub-skills dispatched by this orchestrator operate relative to the worktree path. When assembling a context envelope for a worktree-scoped sub-skill, include:

```
"Your working directory is <worktree_path>. All file reads and writes resolve relative to that path unless they are absolute paths under .vmodel/.build/."
```

Verdict files written by sub-skills:
- `<worktree_path>/.vmodel/.build/tasks/<task-id>/review-ready.yaml` — written by `render-tests` and `implement-leaf` when ready for review.
- `<worktree_path>/.vmodel/.build/tasks/<task-id>/feedback.yaml` — written by `review-execution` on REJECTED.

The orchestrator reads these files after the sub-skill completes. It does NOT read them into its own context — it checks existence and reads only the `verdict` field to minimize context growth.

---

## Sequential fallback

If `build.parallel.enabled: false` in `config.yaml`, fall back to sequential execution: complete one task fully (render-tests → implement-leaf → review-execution → merge/escalate) before starting the next. Use the same worktree lifecycle rules; just never have more than one worktree active at a time.

---

## Build branch

All task branches (`build/<task-id>`) branch from and merge back to the build branch (`build/run-<build-run-id>`). The build branch is created at INITIALIZE if it does not exist. It is separate from `main`; it collects all task merges during the run.

The build branch is not merged to `main` by this skill. That is a post-pipeline step outside this skill's scope (analogous to `wf-command-ship` in the `wf-skill-orchestrate` pattern).
