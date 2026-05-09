# tasks.yaml — Field-by-Field Semantics

Reference for the structure, allowed values, and invariants of
`.vmodel/.build/tasks.yaml`. This file is produced by `vmodel-skill-plan-build`
and consumed by `vmodel-skill-orchestrate-build`.

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
| `files_to_touch` | list | yes | Always `[]` when emitted by the planner. The implement-leaf skill populates this after reading the DD. Do not pre-populate. |
| `depends_on` | list | no | Ordered list of dependency edges. See below. Empty list if no dependencies. |
| `estimates.complexity` | string | yes | One of: `low`, `medium`, `high`. Derived via the complexity heuristic in `references/dependency-inference.md §complexity-heuristic`. |
| `status` | string | yes | Always `pending` when emitted by the planner. The orchestrator updates this field during execution. |

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

---

## Versioning

If the tasks.yaml schema changes in a future version, `version` increments.
The orchestrator checks `version: 1` before consuming. A mismatch halts the
orchestrator with: "tasks.yaml version mismatch — re-run `/vmodel-skill-plan-build`."
