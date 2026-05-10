# tasks.yaml — Field-by-Field Semantics

Reference for the structure, allowed values, and invariants of
`.vmodel/.build/tasks.yaml`. This file is produced by `vmodel-skill-plan-build`
and consumed by `vmodel-skill-orchestrate-build`.

---

## Contents

- [Top-level fields](#top-level-fields)
- [`tasks` list](#tasks-list)
  - [Task fields](#task-fields)
  - [`depends_on` entry fields](#depends_on-entry-fields)
- [`stages` list](#stages-list)
- [`branch_test_stages` list](#branch_test_stages-list)
- [`root_test_stage`](#root_test_stage)
- [Status values](#status-values)
- [Invariants (schema-level)](#invariants-schema-level)
- [Versioning](#versioning)

---

## Top-level fields

```yaml
version: 1
build_run_id: <string>
plan_date: <YYYY-MM-DD>
project: <string>
```

| Field | Type | Required | Description |
|---|---|---|---|
| `version` | integer | yes | Schema version. Always `1` for this skill version. |
| `build_run_id` | string | yes | Stable identifier for this plan run. Format: `<YYYY-MM-DD>-<6-char-hex>`. Stable across re-reads; regenerated only when the planner re-runs. |
| `plan_date` | string | yes | ISO-8601 date the plan was generated. |
| `project` | string | yes | Copied from `.vmodel/config.yaml → project`. Used in log messages and orchestrator reports. |

---

## `tasks` list

Each entry is one leaf-implementation task.

```yaml
tasks:
  - id: build-app-checkout
    scope: app/checkout
    type: leaf-implementation
    detailed_design: DD-app-checkout
    testspec: TS-app-checkout
    governing_adrs: []
    acceptance_criteria:
      - "TS-app-checkout.case-001: validates positive cart total"
    context_to_load:
      - specs/app/checkout/detailed_design.md
      - specs/app/checkout/testspec.md
      - specs/app/architecture.md
      - .vmodel/references/**
    out_of_scope:
      - "Do not modify any file under specs/ — spec artifacts are read-only during build."
      - "Do not modify rendered test files in this leaf's worktree to make tests pass — if a test is wrong, escalate via build-blocked.yaml with blocker_type: test-defect."
      - "Do not implement features absent from the DD's Public Interface — gold-plating is a contract violation."
      - "Do not modify other leaves' source implementations — sibling and dependency leaves are the responsibility of their own implement-leaf invocations."
    files_to_touch: []
    depends_on:
      - id: build-app-cart
        strength: critical
    estimates:
      complexity: medium
    status: pending
```

### Task fields

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Unique task identifier. Format: `build-<scope-flattened>` (slashes → hyphens). Stable across re-plans if scope path doesn't change. |
| `scope` | string | yes | Scope path relative to `scope_root`. Example: `app/checkout`. |
| `type` | string | yes | Always `leaf-implementation` for tasks in the `tasks` list. |
| `detailed_design` | string | yes | ID of the leaf's `detailed_design.md` artifact (from its front-matter `id` field). |
| `testspec` | string | yes | ID of the leaf's `testspec.md` artifact. |
| `governing_adrs` | list | no | IDs of ADRs governing this leaf. Copied from the DD's `governing_adrs` front-matter field. Empty list if none. |
| `acceptance_criteria` | list of strings | yes | One entry per TestSpec case in the leaf's `testspec.md`. Format: `"<TS-id>.<case-id>: <case title>"` (or `"<TS-id>.<case-id>"` if the case lacks a `title`). Mechanical derivation from testspec cases. Plan-build populates; orchestrator passes through to `current-task.yaml`; implement-leaf reads but does not modify; review-execution uses to confirm coverage. May be empty only when the leaf's testspec has zero cases — but those leaves are excluded by refusal B, so in practice non-empty. |
| `context_to_load` | list of file paths | yes | Read-only allowlist of files implement-leaf is permitted to consult. Mechanical derivation from spec tree (see "Derivation rules for `context_to_load`" below). Plan-build populates; implement-leaf MUST refuse to read source files outside this list (project source files implementing the scope are read implicitly and may be opened for refactor — see implement-leaf's enforcement rules). Never empty. |
| `out_of_scope` | list of strings | yes | Declarative "do NOT" statements that constrain implement-leaf. Standard set populated verbatim by plan-build (see "Standard `out_of_scope` entries" below). The fix-mode entry is appended by the orchestrator at fix-mode dispatch. Never empty. |
| `files_to_touch` | list | yes | Always `[]` when emitted by the planner. The implement-leaf skill populates this after reading the DD. Do not pre-populate. |
| `depends_on` | list | no | Ordered list of dependency edges. See below. Empty list if no dependencies. |
| `estimates.complexity` | string | yes | One of: `low`, `medium`, `high`. Derived via the complexity heuristic in `references/dependency-inference.md §complexity-heuristic`. |
| `status` | string | yes | Always `pending` when emitted by the planner. The orchestrator updates this field during execution. |

#### Derivation rules for `context_to_load`

Plan-build populates this list mechanically — no inference, no fabrication:

1. The leaf's own DD: `specs/<scope>/detailed_design.md`.
2. The leaf's own TestSpec: `specs/<scope>/testspec.md`.
3. The parent ARCH (when `parent_scope` is non-empty): `specs/<parent_scope>/architecture.md`.
4. For every entry in `governing_adrs`: the resolved ADR file path. Use the path from the ADR's front-matter when resolvable; otherwise emit a glob `**/adrs/<adr-id>.md` and surface the unresolved path as an ambiguity in the plan report.
5. For every entry in `depends_on[]`: the dependency leaf's DD and TestSpec — `specs/<dep-scope>/detailed_design.md` and `specs/<dep-scope>/testspec.md`. Interfaces must be readable to wire correctly.
6. The shared references directory glob: `.vmodel/references/**`.

No other files are added by the planner. Adding files outside this derivation set is refusal E (see SKILL.md Hard Refusals).

#### Standard `out_of_scope` entries

Plan-build emits this fixed set verbatim on every leaf task. No paraphrasing.

1. `"Do not modify any file under specs/ — spec artifacts are read-only during build."`
2. `"Do not modify rendered test files in this leaf's worktree to make tests pass — if a test is wrong, escalate via build-blocked.yaml with blocker_type: test-defect."`
3. `"Do not implement features absent from the DD's Public Interface — gold-plating is a contract violation."`
4. `"Do not modify other leaves' source implementations — sibling and dependency leaves are the responsibility of their own implement-leaf invocations."`

A fifth entry is appended by the orchestrator at fix-mode dispatch (attempt > 1):

5. `"Do not weaken, disable, or delete tests to satisfy feedback — escalate as ESC if the feedback is itself wrong."`

This entry is NOT in plan-build's output — only the orchestrator adds it, and only on fix-mode dispatch.

### `depends_on` entry fields

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Task id of the dependency (`build-<scope>`). |
| `strength` | string | yes | `critical` or `helpful`. See `references/dependency-inference.md §strength-summary`. |

**Invariant:** Every `id` in a `depends_on` list must reference a task that
appears in the same `tasks` list. Forward references are allowed (the
referenced task may appear later in the list). The planner validates this
before emitting.

---

## `stages` list

Topological grouping. Each stage contains task IDs whose dependencies are all
satisfied by prior stages.

```yaml
stages:
  - stage_id: 1
    tasks: [build-app-cart, build-app-pricing]
  - stage_id: 2
    tasks: [build-app-checkout]
```

| Field | Type | Description |
|---|---|---|
| `stage_id` | integer | 1-indexed. Strictly increasing. |
| `tasks` | list of strings | Task IDs assigned to this stage. |

**Invariant:** Every task id in the `tasks` list must appear exactly once
across all stages. No task is in two stages simultaneously.

**Invariant:** All dependencies of a task in stage N are covered by tasks in
stages 1 through N-1. Intra-stage dependencies are not permitted (would
indicate a cycle that the planner should have caught).

---

## `branch_test_stages` list

One entry per branch scope (non-leaf scope with an `architecture.md`).
Ordered deepest-first (by path depth), shallowest last. Root scope is not
included here — it is in `root_test_stage`.

```yaml
branch_test_stages:
  - scope: app/payments
    type: branch-integration
    architecture: ARCH-app-payments
    testspec: TS-app-payments
    after_stage: 2
  - scope: app
    type: branch-integration
    architecture: ARCH-app
    testspec: TS-app
    after_stage: 3
```

| Field | Type | Required | Description |
|---|---|---|---|
| `scope` | string | yes | Branch scope path relative to `scope_root`. |
| `type` | string | yes | Always `branch-integration`. |
| `architecture` | string | yes | ID of the branch's `architecture.md` artifact. |
| `testspec` | string | no | ID of the branch's `testspec.md`. Omit if no testspec exists for this branch. |
| `after_stage` | integer | yes | The branch integration test runs after this implementation stage completes. Set to the highest stage number whose tasks are children of this branch scope. |

**Ordering rationale:** Deepest branches are tested first because they verify
smaller sub-systems before wider integration. This minimises the blast radius
of a failure at the branch level — a failure in a deep branch is isolated
before testing the parent branch.

---

## `root_test_stage`

Exactly one entry. Emitted even if no root testspec exists (field omitted in
that case).

```yaml
root_test_stage:
  scope: ""
  type: root-system
  architecture: ARCH
  testspec: TS
  requirements: REQS
  root_product: PD
  after_stage: 3
```

| Field | Type | Required | Description |
|---|---|---|---|
| `scope` | string | yes | Always `""` (empty string — the root scope). |
| `type` | string | yes | Always `root-system`. |
| `architecture` | string | no | Root architecture artifact ID. Omit if absent. |
| `testspec` | string | no | Root testspec artifact ID. Omit if absent. |
| `requirements` | string | no | Root requirements artifact ID. Omit if absent. |
| `root_product` | string | no | Root product artifact ID (`pd`, `needs`, or `pb` — per config). Omit if absent. |
| `after_stage` | integer | yes | Equal to the total number of implementation stages. The root system test runs last. |

---

## Status values

The planner emits only `pending`. The orchestrator may write these values:

| Value | Set by | Meaning |
|---|---|---|
| `pending` | planner | Not yet started. |
| `in_progress` | orchestrator | Currently building/testing. |
| `completed` | orchestrator | Build + review approved. |
| `failed` | orchestrator | Max retries exhausted or unrecoverable error. |
| `blocked` | orchestrator | A dependency failed or was blocked. |
| `design_issue` | orchestrator | Halted — architectural contradiction surfaced. |

The planner does not read or mutate these beyond setting the initial `pending`.

---

## Invariants (schema-level)

1. `build_run_id` is unique per plan invocation. Regenerated on each planner run.
2. Task `id` values are unique within the `tasks` list.
3. Every `depends_on[].id` resolves to a task in the same `tasks` list.
4. Stage `tasks` arrays are non-overlapping and collectively cover all task IDs.
5. `after_stage` in branch and root stages is ≤ `max(stages[].stage_id)`.
6. `files_to_touch` is `[]` in planner output — never pre-populated.
7. `acceptance_criteria` is non-empty on every leaf task (leaves with zero TestSpec cases are excluded by refusal B).
8. `context_to_load` is non-empty on every leaf task (rules 1, 2, and 6 above always apply).
9. `out_of_scope` contains the four standard entries verbatim (the fifth fix-mode entry is added by the orchestrator, not the planner).

---

## Versioning

If the tasks.yaml schema changes in a future version, `version` increments.
The orchestrator checks `version: 1` before consuming. A mismatch halts the
orchestrator with: "tasks.yaml version mismatch — re-run `/vmodel-skill-plan-build`."
