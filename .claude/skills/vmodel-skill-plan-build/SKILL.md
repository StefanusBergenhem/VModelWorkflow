---
name: vmodel-skill-plan-build
description: Derive the build-flow task DAG from the spec tree — no human-authored sprint. Walks the architecture artifacts, finds leaf scopes (those with detailed_design.md + testspec.md), infers dependencies from interface usage and ADR ordering, topologically sorts into stages, emits .vmodel/.build/tasks.yaml. Branch and root test stages also planned. Use when starting a build run after spec authoring is complete or partial. Triggers — plan build, derive tasks, build the task DAG, schedule build stages, prepare implementation plan.
type: skill
---

# vmodel-skill-plan-build

Derive the build-flow task DAG from the spec tree. Walk architecture artifacts,
find leaf scopes (those with `detailed_design.md` + `testspec.md`), infer
dependencies from interface usage and ADR ordering, topologically sort into
stages, and emit `.vmodel/.build/tasks.yaml`.

The skill is self-contained. All dependency-inference rules, tasks.yaml schema
semantics, and the output template live in the `references/` and `templates/`
directories.

## When to use

Activate this skill when the user asks to:

- Plan a build run from the current spec tree
- Derive the task DAG from a (complete or partially complete) spec tree
- Build the implementation task list / schedule
- Prepare tasks.yaml before running `vmodel-skill-orchestrate-build`
- Re-plan after spec changes (new leaves added, dependencies changed)

Do **not** activate this skill for:

- Executing or orchestrating the build — that is `vmodel-skill-orchestrate-build`
- Authoring spec artifacts — use the appropriate author skills
- Reviewing or auditing tasks.yaml — that is a human review step

## Inputs

Expected upstream context (ask if missing):

- **`.vmodel/config.yaml`** — project name, `scope_root`, `root_product.type`,
  build-flow model/parallel settings. HALT if absent (refusal A).
- **Spec tree under `scope_root/`** — the directory tree of authored spec
  artifacts. Partially-complete trees are allowed; under-specified leaves are
  excluded with a warning (refusal B).

## Output

A single YAML file: `.vmodel/.build/tasks.yaml`.

Structure and field-by-field semantics: `references/tasks-schema.md`.
Canonical template: `templates/tasks.yaml.tmpl`.

## Authoring procedure

Execute these steps in order.

### Step 1 — Load config

Read `.vmodel/config.yaml`. Extract:
- `project` (name)
- `scope_root` (default: `specs/`)
- `root_product.type` (`pd` | `needs` | `pb`)

If `.vmodel/config.yaml` does not exist → HALT (refusal A). Tell the user to
run `/vmodel-init` first.

### Step 2 — Walk the spec tree

Walk `<scope_root>/` recursively, depth-first. For each directory encountered:

**Leaf candidate** — directory has `detailed_design.md`:
1. Parse YAML front-matter from `detailed_design.md`. Extract: `id`, `scope`,
   `parent_scope`, `parent_architecture`, `governing_adrs`, `derived_from`.
2. Check for sibling `testspec.md`. If absent → emit warning, exclude this
   leaf (refusal B). Log: `WARN: <scope>/testspec.md missing — leaf excluded`.
3. Parse `testspec.md` front-matter. Extract `id`.
4. Record as a leaf candidate with all extracted fields.

**Branch** — directory has `architecture.md` but not `detailed_design.md`:
1. Parse `architecture.md` front-matter. Extract `id`, `scope`.
2. Check for sibling `testspec.md`. If present, extract its `id`.
3. Record as a branch scope for later branch-test-stage generation.

**Root** — `scope_root` itself: record root artifacts if they exist
(`requirements.md`, `testspec.md`, and the root product file per
`root_product.type`).

### Step 3 — Infer dependency edges

For each leaf candidate, infer dependency edges using the rules in
`references/dependency-inference.md`.

Summary of rules applied here:

1. **Interface-production rule** — read the leaf's `parent_architecture` field.
   Load that Architecture artifact. In its Decomposition section, find which
   sibling leaves produce interfaces this leaf consumes. Each producing leaf
   becomes a `depends_on` edge with `strength: critical`.

2. **ADR-ordering rule** — for each ADR in the leaf's `governing_adrs`, check
   whether the ADR body contains explicit sequencing language (see
   `references/dependency-inference.md §ADR-ordering signals`). Derive
   `strength: helpful` edges for any ordering constraints found.

3. **Ambiguity protocol** — if interface usage is unclear (interface declared
   in Architecture but no consumer named), do NOT add a `critical` edge. Add
   a `helpful` edge and record the ambiguity in the plan report. Never guess
   `critical`.

→ See `references/dependency-inference.md` for the full inference rule set.

### Step 4 — Detect cycles

Run a standard DFS-based cycle check on the dependency graph (all leaf nodes
plus their dependency edges). If a cycle is found:
- HALT immediately.
- Report the cycle in full: list every edge in the cycle by scope name.
- Do not emit `tasks.yaml`.
- Instruct the user to resolve the circular dependency in the Architecture
  artifacts before re-running.

Never silently break a cycle.

### Step 5 — Topological sort into stages

Assign each leaf to the earliest stage where all its dependencies are
satisfied by prior stages:

- **Stage 1**: all leaves with no dependencies (or only completed-leaf
  dependencies from a prior partial run).
- **Stage N**: all leaves whose `depends_on` set is fully covered by stages
  1 through N-1.
- Tasks within a stage have no intra-stage dependencies — they are safe to
  execute in parallel.

Assign a `complexity` estimate per leaf using the heuristic in
`references/dependency-inference.md §complexity-heuristic`. Default: `medium`.

### Step 6 — Assign task IDs

Each leaf task gets id: `build-<scope-flattened>` where `<scope-flattened>`
replaces `/` with `-`. Example: scope `app/checkout` → id `build-app-checkout`.

### Step 7 — Build branch test stages

For each branch scope (from Step 2), emit one `branch_test_stages` entry.
Order: deepest branches first (highest path depth), shallowest last, root
always last (becomes `root_test_stage`).

Each branch entry references:
- `scope`: the branch scope path
- `type: branch-integration`
- `architecture`: the branch Architecture artifact id
- `testspec`: the branch TestSpec artifact id (if present; else omit)
- `after_stage`: the number of the last implementation stage whose scopes are
  children of this branch

### Step 8 — Build root test stage

Emit one `root_test_stage` entry using the root scope artifacts discovered in
Step 2. `after_stage` = total number of implementation stages.

### Step 9 — Set build_run_id and plan_date

Generate a `build_run_id` using the format `<YYYY-MM-DD>-<6-char-hex>` (e.g.,
`2026-05-09-a3f7c1`). Use today's date from context; generate the hex suffix
as a short pseudo-unique discriminator derived from the project name and task
count. Use `plan_date: <YYYY-MM-DD>`.

### Step 10 — Emit tasks.yaml

Fill `templates/tasks.yaml.tmpl` with all gathered data. Write to
`.vmodel/.build/tasks.yaml`. Create the directory `.vmodel/.build/` if it does
not exist.

Ensure `files_to_touch: []` on every leaf task — the implement-leaf skill
populates this field; the planner leaves it empty.

### Step 11 — Print plan report

Print a compact human-readable summary:

```
=== vmodel-skill-plan-build complete ===

  Project:        <name>
  Leaves found:   <N> (<M> excluded — missing testspec)
  Stages:         <count>
  Branch stages:  <count>
  Root stage:     yes
  Ambiguities:    <count> (see tasks.yaml — marked strength: helpful)
  Output:         .vmodel/.build/tasks.yaml

Excluded leaves:
  - <scope>: testspec.md missing

Dependency ambiguities:
  - <scope>: interface <iface> declared in <arch-id> but no explicit consumer named

Next step: run /vmodel-skill-orchestrate-build
```

## Hard refusals

**A — Config absent.** Refuse to plan if `.vmodel/config.yaml` does not exist.
The config provides `scope_root`, `project` name, and build-flow model settings
that shape the output. Without it the plan cannot be rooted. Tell the user to
run `/vmodel-init` first.

**B — Leaf without TestSpec excluded.** A leaf with `detailed_design.md` but
no `testspec.md` is not buildable — the build workflow cannot derive
verification targets for it. Exclude it from tasks with a logged warning.
Do not fabricate a testspec reference; do not silently include it.

**C — No fabricated dependencies.** If interface usage cannot be determined
from the Architecture artifact (interface exists but consumption is unstated),
default to `strength: helpful` and surface the ambiguity. Never promote an
ambiguous dependency to `critical`. `critical` means: building A before B is
mandatory for the build to succeed; `helpful` means: preferred but the build
can proceed without it.

**D — No cycle breaking.** If the dependency graph contains a cycle, HALT and
report. Do not silently drop edges to break cycles. The cycle represents a
real architectural contradiction that must be resolved in the spec.

## HALT conditions

1. **`.vmodel/config.yaml` absent** — refusal A. Ask user to run `/vmodel-init`.
2. **Cycle in dependency graph** — refusal D. Report cycle edges, halt, wait
   for spec correction.
3. **Scope tree empty or no leaves found** — no implementation tasks can be
   planned. Report: "No buildable leaf scopes found under `<scope_root>/`.
   Author at least one leaf scope (with `detailed_design.md` + `testspec.md`)
   before planning a build."
4. **tasks.yaml write fails** — report the error (permission, path), do not
   leave a partial file. Suggest creating `.vmodel/.build/` manually if the
   directory is missing.

When halting, emit a structured handover: what was discovered, what is
missing, what the user must do to unblock.

## Pointers

- `references/dependency-inference.md` — full rules for inferring edges
  (interface-production, ADR-ordering, ambiguity protocol, complexity
  heuristic)
- `references/tasks-schema.md` — tasks.yaml structure with field-by-field
  semantics, allowed values, invariants
- `templates/tasks.yaml.tmpl` — canonical output template
- `.vmodel/references/authoring-discipline.md` — cross-cutting authoring rules
  (config-resolved path; loaded from the project's own `.vmodel/references/`)
