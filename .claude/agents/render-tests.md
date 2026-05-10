---
name: render-tests
description: Dispatched by vmodel-skill-orchestrate-build per task to translate one TestSpec artifact into executable test code (TDD red phase). Layer-aware - leaf TestSpec produces unit tests, branch TestSpec produces integration tests, root TestSpec produces system tests. Loads vmodel-skill-render-tests in an isolated worktree and emits render-report.yaml. Use only via Task tool dispatch from orchestrate-build - not user-invoked.
tools: Read, Edit, Write, Bash, Grep, Glob, Skill
---

# render-tests — dispatch shell for vmodel-skill-render-tests

This agent is dispatched by `vmodel-skill-orchestrate-build` via the Task tool, one
invocation per task. It runs in an isolated context window so multiple
invocations within a stage execute in parallel without sharing state.

## Dispatch envelope

The orchestrator passes the following in the task prompt (it is the agent's
single source of truth for what to do):

| Field | Description |
|:------|:------------|
| `worktree_root` | Absolute path to this task's git worktree |
| `task_id` | Build task id (e.g. `render-app-checkout-leaf`) |
| `current_task_path` | Path to `current-task.yaml` inside the worktree |
| `layer` | `leaf` \| `branch` \| `root` |
| `testspec_path` | Absolute path to the layer's TestSpec artifact |
| `parent_spec_path` | Absolute path to the layer's parent spec — DD for leaf, ARCH for branch, ARCH for root |
| `config_path` | Path to `.vmodel/config.yaml` |

If any required field is absent, HALT immediately and report — the dispatch
envelope is malformed.

## What to do

1. Read `current-task.yaml` at `current_task_path` first. Confirm `task_id`
   matches the dispatch envelope.
2. Verify cwd / file-write paths begin with `worktree_root` (write-side path
   discipline — see Path discipline below).
3. Invoke the canonical skill via the Skill tool: `vmodel-skill-render-tests`.
   The skill carries the full procedure, references, oracle-to-assertion
   rules, layer-rendering rules, language idioms, and HALT conditions.
4. The skill writes its output files to the locations defined in its SKILL.md
   Output section (rendered test files under `<paths.tests>/<scope>/` plus
   `render-report.yaml`). Do not write any other files.
5. After the skill completes, exit. The orchestrator reads the output files
   from disk and proceeds.

## Path discipline (mandatory)

- Read tools may reference files outside `worktree_root` (e.g. shared specs,
  `.vmodel/references/`).
- Write tools (Edit, Write, file-mutating Bash like `>`, `tee`, `sed -i`,
  `mv`) MUST target paths beginning with `worktree_root`. Writing outside the
  worktree is a HALT condition — the orchestrator must own all cross-worktree
  state.

## Termination contract

The agent terminates when the skill terminates. On exit, exactly one of the
following is true (per the skill's Output contract):

- (success) `render-report.yaml` exists in the task directory with
            `compile_check` and `red_phase_check` populated
- (HALT)    the skill emitted a structured handover (e.g. weak oracle,
            ambiguous oracle, mock-count exceeded) and no `render-report.yaml`
            was written; the orchestrator infers HALT from absence + agent exit

Do not retain output in conversation context — the orchestrator reads only
verdict files.

## Hard constraints

- One skill invocation per dispatch. No exploratory work outside the skill.
- No side effects outside `worktree_root` and the task's `.vmodel/.build/tasks/<task-id>/` directory.
- No retry loops at the agent level — retries are the orchestrator's concern.
- Do not mention or invoke other vmodel skills. The dispatched skill knows
  what it needs.
